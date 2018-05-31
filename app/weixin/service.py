# -*- coding: utf-8 -*-
"""
Created by suun on 5/26/2018
"""
from urllib.parse import unquote
from packages.service.xiaoice import get_instant_msg
from packages.service.customer_service import BM25
from .middleware import make_text_msg, make_img_msg, get_media_id_from_url


bm = BM25()
bm.build_from_file("data/2013.txt")


def xiaoice_response(msg):
    instant_message = get_instant_msg(msg['Content'], msg['FromUserName'])
    if len(instant_message['ReplyText']):
        return make_text_msg(msg, unquote(instant_message['ReplyText']))
    elif len(instant_message['ImageUrl']):
        media_ret = get_media_id_from_url(instant_message['ImageUrl'], 'image')
        if media_ret['status']:
            return make_img_msg(msg, media_ret['media_id'])
        else:
            return ""


def customer_service_response(msg):
    ret = str('\n'.join([item[0] for item in bm.sim_all(msg['Content'])]))
    return make_text_msg(msg, ret)
    # return make_text_msg(msg, "magic number: o88KNt2-akQ3dkNuetObVHW69KfY")
