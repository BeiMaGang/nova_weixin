# -*- coding: utf-8 -*-
"""
Created by suun on 5/17/2018
"""
import os
import time
from .url import Url
from .communicate import Communicate
from .token import AccessToken
from .res_format import MsgFormat


def send_template_msg(appid, secret, data):
    token_ret = AccessToken.get(appid, secret)
    print(token_ret)
    if token_ret['status']:
        access_token = token_ret['access_token']
        url = Url.send_template_msg.format(access_token=access_token)
        return Communicate.post(url, data.encode('utf-8'))
    else:
        return token_ret


def get_temp_media_from_file(access_token, filename, media_type):
    upload_url = Url.upload_temp_media.format(access_token=access_token, type=media_type)
    upload_ret = Communicate.post(upload_url, files={
        'media': open(filename, 'rb')
    })
    os.remove(filename)
    if 'errcode' not in upload_ret:
        return {
            'status': 1,
            'media_id': upload_ret['media_id']
        }
    else:
        return {'status': 0}
