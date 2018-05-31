# -*- coding: utf-8 -*-
"""
Created by suun on 5/14/2018
"""
import time
from .url import Url
from .communicate import Communicate


class AccessToken(object):
    last_time = 0
    access_token = None

    @staticmethod
    def get(appid, secret):
        now_time = time.time()
        if now_time - AccessToken.last_time < 1800:
            return {'status': 1, 'access_token': AccessToken.access_token}
        else:
            url = Url.token.format(appid=appid, appsecret=secret)
            res = Communicate.get(url)
            if 'errcode' in res:
                return {'status': 0, 'errmsg': res.get('errmsg'), 'errcode': res.get('errcode')}
            else:
                access_token = res.get('access_token')
                AccessToken.last_time = now_time
                AccessToken.access_token = access_token
                return {'status': 1, 'access_token': access_token}
