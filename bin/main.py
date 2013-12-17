#!/usr/bin/python

import os, web, json
import logging, logging.handlers

class MainUtil:
  logger = None

  def __init__(self, conf_path):
    with open(conf_path) as f:
      self.conf = json.load(f)
    self.loggers = {}

  def getTemplate(self, path):
    from Cheetah.Template import Template
    tmpl_path = "%s/%s" % (self.conf['tmpl'], path)
    t = None
    with open(tmpl_path) as f:
      t = Template(f.read())
    return t

  def getLogger(self, name):
    if not name in self.loggers:
      l = logging.getLogger(name)
      h = logging.handlers.RotatingFileHandler(self.conf['log']+"/"+name+".log", maxBytes=1048576, backupCount=5)
      if 'log_format' in self.conf:
        f = logging.Formatter(self.conf['log_format'])
        h.setFormatter(f)
      l.addHandler(h)
      l.setLevel(logging.DEBUG)
      if 'log_default_level' in self.conf:
        l.setLevel(int(self.conf['log_default_level']))
      self.loggers[name] = l

    return self.loggers[name]

main_util = MainUtil("etc/main.json")
main_urls = []
main_logger = main_util.getLogger(__name__)

class CgiBase(type):
  def __init__(klass, name, bases, attrs):
    main_urls.append(attrs["url"])
    main_urls.append("%s.%s" % (klass.__module__, name))

def loadAllCgi():
  for c in os.listdir(os.getcwd() + "/" + main_util.conf['cgi_dir']):
    name, ext = os.path.splitext(c)
    if name.startswith('cgi_') and ext == '.py':
      module = __import__(name)
      main_logger.info("imported %s.py"% (name))

if __name__ == "__main__":
  main_logger.info("MyWeb started.")

  loadAllCgi()

  app = web.application(main_urls, globals())
  main_logger.info("App created, start listening... ")

  app.run()
  main_logger.info("App ended. Bye.")
