#!/usr/bin/env python

import csv
import requests
import json
import urllib
import datetime
import getopt
import sys
import base64
import copy
import hashlib
import hmac
import math
import os
from time import time
from pprint import pprint
from urlparse import urlsplit
from urllib import urlencode

with open('config.json') as config_file:
    config = json.load(config_file)

MY_ORG_ID = config['lvp']['ORG_ID']
MY_ACCESS_KEY = config['lvp']['ACCESS_KEY']
MY_SECRET = config['lvp']['SECRET']

CHANNEL_ID = config['lvp']['CHANNEL_ID'] 

def authenticate_request(http_verb, resource_url, access_key, secret, params = {}):
    # instantiating/cloning params dictionary
    if params == None:
        params = {}
    else:
        params = copy.deepcopy(params)
    
    # Adding necessary items to the dictionary
    params["access_key"] = access_key
    if not "expires" in params:
        params["expires"] = int(math.ceil(time() + 300))


    # Generating signed url and the string to generate the signature from
    parsed_url = urlsplit(resource_url)

    str_to_sign = http_verb.lower() + "|" + parsed_url.hostname.lower() + "|" + parsed_url.path.lower() + "|"
    signed_url = resource_url + "?"

    # Iterating through keys in sorted order to build up the string to sign
    # and the signed url querystring
    items = sorted(params.items())

    for item in items:
        signed_url += urlencode({item[0] : item[1]}) + "&"
        str_to_sign += str(item[0]) + "=" + str(item[1]) + "&"

    # Removing trailing "&"
    str_to_sign = str_to_sign.strip("&")

    # Creating signature
    signature = base64.b64encode(hmac.new(secret.encode("ascii"), str_to_sign.encode("ascii"), hashlib.sha256).digest())
    signature = signature.decode("ascii")

    signed_url += urlencode({"signature" : signature})
    
    return signed_url

def upload_video(file_path, title):
    request_url = "http://api.video.limelight.com/rest/organizations/" + MY_ORG_ID + "/media.json"
    auth_url = authenticate_request("POST", request_url, MY_ACCESS_KEY, MY_SECRET)

    params = {'title' : title, 'add_to_channel': CHANNEL_ID,}

    files = {'media_file': open(file_path, 'rb')}
    starttime = datetime.datetime.now()
    headers = {'Content-Disposition': 'form-data; name="media_file"; filename="%s"' % file_path}

    r = requests.post(auth_url, files=files, data=params, headers=headers)

    endtime = datetime.datetime.now()
    totaltime = endtime - starttime
    elapsed_time = (totaltime.total_seconds())

    return_json = r.json()

    try:
        media_id = return_json['media_id']
    except KeyError:
        return "Video upload Failed!" 

    os.remove(file_path)
    return "Upload completed!"
