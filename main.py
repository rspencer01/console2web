import sys
import random
import time
import os
import argparse
import subprocess
import markdown
import tempfile
from HtmlPipe import HtmlPipe

parser = argparse.ArgumentParser()
parser.add_argument('cmd')
parser.add_argument('--title', '-t', required=False, default=None)
parser.add_argument('--readme', '-r', required=False, default=None)
parser.add_argument('--favicon', '-i', required=False, default=None)

args = parser.parse_args()

if not args.title:
  args.title = args.cmd.split()[0]

if not args.readme:
  args.readme = os.path.dirname(args.cmd.split()[0])+"/README.md"
  if not os.path.exists(args.readme):
    args.readme = None

if not args.favicon:
  args.favicon = os.path.dirname(args.cmd.split()[0])+"/favicon.png"
  if not os.path.exists(args.favicon):
    args.favicon = None

sys.argv = ['', '8080']
import web
web.config.debug = False

class Gamestate(object):
  def __init__(self,sessionid):
    directory = tempfile.mkdtemp()
    self.stdout_filename = os.path.join(directory, str(sessionid) + '.stdout')
    self.stdin_filename = os.path.join(directory, str(sessionid) + '.stdin')
    os.mkfifo(self.stdout_filename)
    os.mkfifo(self.stdin_filename)

    self.stdout_us = os.open(self.stdout_filename,os.O_RDONLY|os.O_NONBLOCK)
    self.stdout_them = os.open(self.stdout_filename,os.O_RDWR)
    self.stdin_them = os.open(self.stdin_filename,os.O_RDWR)
    self.stdin_us = os.open(self.stdin_filename,os.O_RDWR)

    self.p = subprocess.Popen(args.cmd.split(), stdout=self.stdout_them, stdin=self.stdin_them)

    self.pipe = HtmlPipe(self.stdout_us,self.stdin_us)

  def getNext(self):
    stdout = self.pipe.html_format()
    if self.p.poll() is None:
      self.end_process()
    return stdout

  def giveString(self, inpt):
    self.pipe.write(inpt)

  def end_process(self):
    os.close(self.stdout_us)
    os.close(self.stdout_them)
    os.close(self.stdin_them)
    os.close(self.stdin_us)
    os.remove(self.stdout_filename)
    os.remove(self.stdin_filename)

class Readme:
  def GET(self):
    if args.readme is None:
      return "This project has no README.md"
    md = open(args.readme).read()
    return render.readme(markdown.markdown(md))

gamestates = {}

urls = (
       '/', 'index',
       '/reply', 'reply',
       '/js', 'js',
       '/kill', 'kill',
       '/readme', 'Readme',
       '/favicon', 'favicon',
       )
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'id': None})
render = web.template.render('./')

class index:
  def GET(self):
    if session.id is None:
      session.id = random.randint(0,1000000)
      gamestates[session.id] = Gamestate(session.id)
    return render.main(session, args.title, args.readme, args.cmd)

class reply:
  def POST(self):
    if session.id is None:
      return "ERROR: no session ID"
    if session.id not in gamestates:
      gamestates[session.id] = Gamestate(session.id)
    gamestate = gamestates[session.id]
    gamestate.giveString(web.input().response)
    time.sleep(1)
    rep = gamestate.getNext()
    return rep

class favicon:
  def GET(self):
    return open(args.favicon).read()

class kill:
  def POST(self):
    session.kill()

class js:
  def GET(self):
    return open('jquery.min.js').read()

if __name__ == "__main__":
  app.run()
