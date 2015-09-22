import os
__all__ = (
        "get_pictures",
        "get_picture_dirs",
        "get_pictures_dict",
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
