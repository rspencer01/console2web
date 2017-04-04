import time

colours = {
  'color:#000;' : "0;30",
  'color:#000;font-weight:bold;;' : "1;30",
  'color:#C00;' : "0;31",
  'color:#C00;font-weight:bold;' : "1;31",
  'color:#0C0;' : "0;32",
  'color:#0C0;font-weight:bold;' : "1;32",
  'color:#AA0;' : "0;33",
  'color:#AA0;font-weight:bold;' : "1;33",
  'color:#00C;' : "0;34",
  'color:#00C;font-weight:bold;' : "1;34",
  'color:#D0D;' : "0;35",
  'color:#D0D;font-weigth:bold;' : "1;35",
  'color:#0DD;' : "0;36",
  'color:#0DD;font-weight:bold;' : "1;36",
  'color:#AAA;' : "0;37",
  'color:#DDD;' : "1;37",
  }

class HtmlPipe(object):
  def __init__(self):
    self.stdout = ""
    self.stdin = ""

  def write(self, string):
    self.stdout += string

  def readline(self):
    while self.stdin == "":
      time.sleep(1)
    return self.stdin

  def flush(self):
    pass

  def clear_stdout(self):
    self.stdout = ""

  def html_format(self):
    stdout = self.stdout
    stdout = stdout.replace(' ','&nbsp')
    stdout = '<span style=\'color:#AAA;\'>' + stdout + '<span>'
    stdout = stdout.replace('\n','<br>')
    for colour in colours:
      stdout = stdout.replace('\033[0{}m'.format(colours[colour]),'</span><span style=\'{};\'>'.format(colour))


    return stdout
