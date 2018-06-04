# -*- coding: utf-8 -*-
"""
Created by suun on 5/26/2018
"""
from urllib.parse import unquote
from packages.service.xiaoice import get_instant_msg, tuling_reply
from packages.service.customer_service import BM25
from .middleware import CustomMsg, ResponseMsg, get_media_id_from_url
from app.config import TULING_API_KEYS

bm = BM25()
bm.build_from_file("data/2013.txt")


def xiaoice_response(msg):
    instant_message = get_instant_msg(msg['Content'], msg['FromUserName'])
    if len(instant_message['ReplyText']):
        return ResponseMsg.text(msg, unquote(instant_message['ReplyText']))
    elif len(instant_message['ImageUrl']):
        media_ret = get_media_id_from_url(instant_message['ImageUrl'], 'image')
        if media_ret['status']:
            return ResponseMsg.img(msg, media_ret['media_id'])
        else:
            return ""


def tuling_response(msg):
    is_send = False
    for key in TULING_API_KEYS:
        api_reply = tuling_reply(api_key=key, user_id=msg['FromUserName'], content=msg['Content'])
        if api_reply['status']:
            is_send = True
            for k, v in api_reply['content'].items():
                if k == 'text':
                    CustomMsg.text(msg, v)
                elif k == 'news':
                    CustomMsg.news(msg, v)
            break
    return "" if is_send else xiaoice_response(msg)


def customer_service_response(msg):
    ret = str('\n'.join([item[0] for item in bm.sim_all(msg['Content'])]))
    return ResponseMsg.text(msg, ret)
