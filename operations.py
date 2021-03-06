import os
import subprocess
import thread
from wand.image import Image
from ll_upload import upload_video

__all__ = (
        "get_pictures",
        "get_picture_dirs",
        "get_pictures_dict",
        "strip_underscore",
        "format_pictures_header",
        "get_picture_caption",
        "process_picture_upload",
        "process_video_upload",
)

# Used by Pictures

def get_picture_dirs(location='static/res/photos'):
    dirs = []
    try:
        dirs = [x for x in os.listdir(location) if os.path.isdir(os.path.join(location, x))]
    except OSError as e:
        pass
    return dirs

def get_pictures(location):
    if not location:
        location = 'static/res/photos'
    pics = []
    try:
        pics = [ f for f in os.listdir(location) if os.path.isfile(os.path.join(location, f)) ]
        # Remove any items that are caption files
        pics = [x for x in pics if not ".cpt" in x.lower()]
    except OSError as e:
        pass
    return pics

def get_pictures_dict(location='static/res/photos'):
    dirs = []
    try:
        root_dirs = [x for x in os.listdir(location) if os.path.isdir(os.path.join(location, x))]
        dir_dict = dict.fromkeys(root_dirs)
        for key in dir_dict:
            root_dir = location + "/" + key
            dir_dict[key] = [x for x in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, x))]
    except OSError as e:
        pass
    return dir_dict

def strip_underscore(string):
    return string.replace ("_", " ")

def format_pictures_header(string):
    if string.endswith('/'):
        string = string[:-1]
    string = strip_underscore(string.replace ("static/res/photos/", "").replace("/", " / "))
    return string

def get_picture_caption(pic_filepath):
    print "DEBUG: %s" % pic_filepath
    caption_file = "%s.cpt" % os.path.splitext(pic_filepath)[0]

    try:
        with open(caption_file, 'r') as f:
            caption = f.readline()
    except IOError as e:
        caption = os.path.basename(pic_filepath)
    except:
        caption = "Unexpecter Error!!"

    return caption

def process_picture_upload(file, upload_dir):

    filepath = file.filename.replace('\\', '/')
    filename = filepath.split('/')[-1]
    full_path = upload_dir + filename
    fout = open(full_path, 'w')
    fout.write(file.file.read())
    fout.close()

    with Image(filename=full_path) as original:
        if original.orientation == "right_top":
            original.rotate(90)
            original.save(filename=full_path)
        print "Original Orientation: %s" % original.orientation
        with original.clone() as cloned:
            cloned.resize(65,65)
            cloned.save(filename=upload_dir + "thumbs/" + filename)
            print "Cloned Orientation: %s" % cloned.orientation

def process_video_upload(file, upload_dir, title):

    filepath = file.filename.replace('\\', '/')
    filename = filepath.split('/')[-1]
    full_path = upload_dir + filename
    fout = open(full_path, 'w')
    fout.write(file.file.read())
    fout.close()

    thread.start_new_thread(upload_video, (full_path, title))
