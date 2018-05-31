# -*- coding: utf-8 -*-
"""
Created by suun on 5/17/2018
"""

from .communicate import Communicate
from .url import Url


def get_openid_from_code(code, appid, secret):
    """
    fetch user's openid with code from oauth
    :return:正确返回的json:
               {
               "access_token":"ACCESS_TOKEN",
               "expires_in":7200,
               "refresh_token":"REFRESH_TOKEN",
               "openid":"OPENID",
               "scope":"SCOPE",
               "unionid": "..."
               }
               有错误时返回的json:{"errcode":40029,"errmsg":"invalid code"}
    """
    url = Url.oauth2_token.format(appid=appid, appsecret=secret, code=code)
    ret = Communicate.get(url)
    # print(ret)
    return ret.get('openid', None)
