#!/usr/bin/env python

import web
import os
import sys
import inspect

if __name__ != "__main__":              # mod_wsgi has no concept of where it is
    abspath = os.path.dirname(__file__)
    sys.path.append(abspath)
    os.chdir(abspath)

from operations import *

urls = (
    '/','Default',
    '/(.+)', 'Pictures',
)

t_globals = {
    'get_picture_dirs': get_picture_dirs,
    'get_pictures_dict': get_pictures_dict,
    'strip_underscore': strip_underscore,
    'format_pictures_header': format_pictures_header,
    'get_picture_caption': get_picture_caption,
}

render = web.template.render('template',base='base', globals=t_globals)

class Default:
    def GET(self):
        return render.default()

class Pictures:
    def GET(self, none):
        data = web.input()
        photos_dir = "static/res/photos/%s/" % data.dir
        print "DEBUG (%s::%s): %s" % (self.__class__.__name__, inspect.stack()[0][3], photos_dir)
        return render.pictures(get_pictures(photos_dir), photos_dir)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run() # devel
else:
    application = app.wsgifunc() # apache2 + wsgi
