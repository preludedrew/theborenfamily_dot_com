#!/usr/bin/env python

import web
import os
import sys
import inspect
import datetime
import hashlib
import json

web.config.debug = False
if __name__ != "__main__":              # mod_wsgi has no concept of where it is
    abspath = os.path.dirname(__file__)
    sys.path.append(abspath)
    os.chdir(abspath)

from operations import *

with open('config.json') as config_file:
    config = json.load(config_file)

credentials = config['credentials']

urls = (
    '/','Default',
    '/pictures', 'Pictures',
    '/videos', 'Videos',
    '/login', 'Login',
    '/upload', 'Upload',
    '/failed', 'Failed',
    '/404', 'NotFound',
    '/(.+)', 'Catchall',
)

t_globals = {
    'get_picture_dirs': get_picture_dirs,
    'get_pictures_dict': get_pictures_dict,
    'strip_underscore': strip_underscore,
    'format_pictures_header': format_pictures_header,
    'get_picture_caption': get_picture_caption,
}

app = web.application(urls, globals())
render = web.template.render('template',base='base', globals=t_globals)
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'logged_in': False})
web.config.session_parameters['timeout'] = 60 

class Default:
    def GET(self):
        return render.default()

class Videos:
    def GET(self):
        return render.videos()

class Pictures:
    def GET(self, path=None):
        data = web.input()
        photos_dir = "static/res/photos/%s/" % data.dir
        print "DEBUG (%s::%s): %s" % (self.__class__.__name__, inspect.stack()[0][3], photos_dir)
        return render.pictures(get_pictures(photos_dir), photos_dir)

class Upload:
    def GET(self):
        if session.get('logged_in', False): 
            return render.upload()
        else:
            raise web.seeother("/login") 

    def POST(self):
        picture_dir = '/opt/www/theborenfamily_dot_com/static/res/photos/Uploads/Andrew/'
        pictures = web.webapi.rawinput().get("pictures") 

        videos_dir = '/opt/www/theborenfamily_dot_com/static/res/videos/Uploads/'
        videos = web.webapi.rawinput().get("video_file")
        video_title = web.webapi.rawinput().get("video_title")

        if pictures != None:
            for f in pictures:
	        if f.filename != "":
                    process_picture_upload(f, picture_dir)

        if videos != None:
            process_video_upload(videos, videos_dir, video_title if video_title else videos.filename)

        raise web.seeother('/upload')

class Login:
    def GET(self):
	return render.login()

    def POST(self):
        username = web.input().username
        password = web.input().password
	if username in credentials:
            if credentials[username] == hashlib.md5(password).hexdigest():
                session.logged_in = True
                raise web.seeother("/upload")
            else:
                raise web.seeother("/failed")
        else:
            raise web.seeother("/failed")

class Failed:
    def GET(self):
        return render.failed()

class NotFound:
    def GET(self):
        return render.notfound()

class Catchall:
    def GET(self,path=None):
        raise web.seeother('/404')

if __name__ == "__main__":
    app.run() # devel
else:
    application = app.wsgifunc() # apache2 + wsgi
