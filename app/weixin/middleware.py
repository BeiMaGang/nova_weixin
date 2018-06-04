# -*- coding: utf-8 -*-
"""
Created by suun on 5/25/2018
"""
import requests
import time
import json
from flask import make_response
from packages.utils.wechatAccAPI import (AccessToken, get_temp_media_from_file,
                                         Url, MsgFormat, Communicate)
from app.config import APP_ID, SECRET


def get_media_id_from_url(url, media_type):
    url = str(url)
    response = requests.get(url)
    filename = "temp/%s" % (url.split('/')[-1])
    open(filename, 'wb').write(response.content)
    token_dict = AccessToken.get(appid=APP_ID, secret=SECRET)
    if token_dict['status']:
        access_token = token_dict['access_token']
        return get_temp_media_from_file(access_token, filename, media_type)
    else:
        return {'status': 0}


class ResponseMsg(object):
    @staticmethod
    def __make_msg(data):
        response = make_response(data)
        response.content_type = 'application/xml'
        return response

    @classmethod
    def text(cls, msg, content):
        return cls.__make_msg(MsgFormat.text % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), content))

    @classmethod
    def img(cls, msg, media_id):
        return cls.__make_msg(MsgFormat.image % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), media_id))

    @classmethod
    def news(cls, msg, details):
        """

        :param msg:
        :param details:
        >>>details = [{
        ...    'title': 'Title',
        ...    'description': 'Description',
        ...    'picurl': 'PicUrl',
        ...    'url': 'Url'
        ...}]
        :return: make_response(msg)
        """
        news_front = MsgFormat.news_front % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())), len(details))
        news_middle = ''.join([MsgFormat.news_middle % (
            line['Title'], line['Description'], line['PicUrl'], line['Url']) for line in details])
        return cls.__make_msg(news_front + news_middle + MsgFormat.news_back)


class CustomMsg(object):
    @staticmethod
    def __make_custom_msg(params):
        token_dict = AccessToken.get(appid=APP_ID, secret=SECRET)
        if token_dict['status']:
            url = Url.send_msg.format(access_token=token_dict['access_token'])
            return Communicate.post(
                url, data=json.dumps(params, ensure_ascii=False).encode('utf-8'))

    @classmethod
    def text(cls, msg, content):
        params = {
            'touser': msg['FromUserName'],
            'msgtype': 'text',
            'text': {
                'content': content
            }
        }
        return cls.__make_custom_msg(params)

    @classmethod
    def img(cls, msg, media_id):
        params = {
            'touser': msg['FromUserName'],
            'msgtype': 'image',
            'image': {
                'media_id': media_id
            }
        }
        return cls.__make_custom_msg(params)

    @classmethod
    def news(cls, msg, details):
        params = {
            'touser': msg['FromUserName'],
            'msgtype': 'news',
            'news': {
                'articles': details
            }
        }
        return cls.__make_custom_msg(params)
