# -*- coding: utf-8 -*-
"""
Created by suun on 5/25/2018
"""
import requests
import time
from flask import make_response
from packages.utils.wechatAccAPI import AccessToken, get_temp_media_from_file
from app.config import APP_ID, SECRET
from packages.utils.wechatAccAPI import MsgFormat


def get_media_id_from_url(url, media_type):
    url = str(url)
    response = requests.get(url)
    print(url)
    filename = "temp/%s" % (url.split('/')[-1])
    open(filename, 'wb').write(response.content)
    token_dict = AccessToken.get(appid=APP_ID, secret=SECRET)
    if token_dict['status']:
        access_token = token_dict['access_token']
        return get_temp_media_from_file(access_token, filename, media_type)
    else:
        return {'status': 0}


def make_text_msg(msg, content):
    response = make_response(MsgFormat.text % (msg['FromUserName'], msg['ToUserName'],
                                               str(int(time.time())), content))
    response.content_type = 'application/xml'
    return response


def make_img_msg(msg, media_id):
    response = make_response(MsgFormat.image % (msg['FromUserName'], msg['ToUserName'],
                                                str(int(time.time())), media_id))
    response.content_type = 'application/xml'
    return response
