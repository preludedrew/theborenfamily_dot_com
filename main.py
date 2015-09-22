#!/usr/bin/env python

import web
import os
import sys

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
}

render = web.template.render('template',base='base', globals=t_globals)

class Default:
    def GET(self):
        return render.default()

class Pictures:
    def GET(self, none):
        data = web.input()
        photos_dir = "static/res/photos/%s/" % data.dir
        return render.pictures(get_pictures(photos_dir), photos_dir)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run() # devel
else:
    application = app.wsgifunc() # apache2 + wsgi