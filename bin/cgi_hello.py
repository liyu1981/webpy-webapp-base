from main import CgiBase

class hello:
  __metaclass__ = CgiBase
  url = '/(.*)'

  def GET(self, name):
    from main import main_util

    if not name: 
      name = 'Yu & Minhua'

    main_util.getLogger(__name__).debug("name=%s" % (name))

    tmpl = main_util.getTemplate('hello.html')
    tmpl.name = name;

    return str(tmpl)
