import sys, threading
import random
import time
import os
import argparse
from HtmlPipe import HtmlPipe

parser = argparse.ArgumentParser()
parser.add_argument('module_path')
parser.add_argument('--title', '-t', required=False, default=None)

args = parser.parse_args()

module_head, module_tail = os.path.split(args.module_path)
sys.path.insert(0, module_head)

if not args.title:
  args.title = module_tail.title()

sys.argv = ['', '8080']
import web
web.config.debug = False

class Gamestate(object):
  def __init__(self):
    self.pipe = HtmlPipe()
    exec('import {}'.format(module_tail))
    exec('self.module = {}'.format(module_tail))
    self.module.sys.stdout = self.pipe
    self.module.sys.stdin = self.pipe
    thread = threading.Thread(target=self.module.main)
    thread.daemon = True
    thread.start()

  def getNext(self):
    stdout = self.pipe.html_format()
    self.pipe.clear_stdout()
    return stdout

  def giveString(self, inpt):
    self.pipe.stdin = inpt

gamestates = {}

urls = (
       '/', 'index',
       '/reply', 'reply',
       '/js', 'js',
       '/kill', 'kill',
       )
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'id': None})
render = web.template.render('./')

class index:
  def GET(self):
    if session.id is None:
      session.id = random.randint(0,1000000)
      gamestates[session.id] = Gamestate()
    return render.main(session, args.title)

class reply:
  def POST(self):
    if session.id is None:
      return "ERROR: no session ID"
    if session.id not in gamestates:
      gamestates[session.id] = Gamestate()
    gamestate = gamestates[session.id]
    gamestate.giveString(web.input().response)
    time.sleep(1)
    rep = gamestate.getNext()
    return rep

class kill:
  def POST(self):
    session.kill()

class js:
  def GET(self):
    return open('jquery.min.js').read()

if __name__ == "__main__":
  app.run()
