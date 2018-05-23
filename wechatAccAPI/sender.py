# -*- coding: utf-8 -*-
"""
Created by suun on 5/17/2018
"""
from .url import Url
from .communicate import Communicate


def send_template_msg(access_token, data):
    url = Url.send_template_msg.format(access_token=access_token)
    return Communicate.post(url, data.encode('utf-8'))

