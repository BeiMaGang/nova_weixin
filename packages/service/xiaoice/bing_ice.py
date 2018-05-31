# -*- coding: utf-8 -*-
"""
Created by suun on 5/26/2018
"""

import requests

# old url: http://www.xiaobing.tk/chat.php
XIAOICE_API_URL = "https://www4.bing.com/socialagent/chat"


def get_instant_msg(_query, _id):
    ret = requests.get(XIAOICE_API_URL, params={
        'q': _query,
        'anid': _id
    })
    return ret.json()['InstantMessage']
