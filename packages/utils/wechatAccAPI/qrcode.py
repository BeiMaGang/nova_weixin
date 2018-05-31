# -*- coding: utf-8 -*-
"""
Created by suun on 5/14/2018
"""
from .url import Url
from .communicate import Communicate
import json


def create_ticket(action_name, access_token, scene_id, expire_seconds):
    url = Url.create_qrcode.format(access_token=access_token)
    if action_name != 'QR_SCENE' and action_name != 'QR_LIMIT_SCENE':
        return {'status': -1, 'errcode': 10000, 'errmsg': 'action name error'}
    data = {
        "action_name": action_name,
        "expire_seconds": expire_seconds,
        "action_info":
            {
                "scene": {"scene_id": scene_id}
            }
    }
    res = Communicate.post(url, json.dumps(data, ensure_ascii=False).encode('utf-8'))
    res['status'] = -1 if 'errcode' in res else 1
    return res


def get_qrcode_url(action_name, access_token, scene_id=0, expire_seconds=604800):
    tick = create_ticket(action_name, access_token, scene_id, expire_seconds)
    if tick['status'] == -1:
        return tick
    else:
        return {'status': 1, 'url': Url.download_qrcode.format(ticket=tick.get('ticket'))}
