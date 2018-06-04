# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
"""

以下用到encode的地方均是因为从数据库取出的数据为utf8，否则会出现UnicodeError

"""
from packages.utils.sql import ServiceStatusForm, dbsession, StudentIdBindForm, PhoneBindForm
from .middleware import ResponseMsg
from .service import tuling_response, customer_service_response


def handle_msg(msg):
    if msg['MsgType'] == 'text':
        return __handle_text(msg)
    if msg['MsgType'] == 'event':
        return ResponseMsg.text(msg, __handle_event(msg))


def __handle_text(msg):
    msg_text = msg['Content']
    openid = msg['FromUserName']
    if len(ServiceStatusForm.query.filter_by(openid=openid).all()) == 0:
        dbsession.add(ServiceStatusForm(openid=openid, on_service=False))
    that_row = ServiceStatusForm.query.filter_by(openid=openid).first()

    if '客服' == msg_text:
        if len(StudentIdBindForm.query.filter_by(openid=openid).all()) +\
                len(PhoneBindForm.query.filter_by(openid=openid).all()) > 0:
            that_row.on_service = True
            dbsession.commit()
            return ResponseMsg.text(msg, "您已进入智能客服系统，如果要退出该系统，请发送\"退出客服\"")
        else:
            return ResponseMsg.text(msg, "绑定用户后才可以使用客服功能。")
    elif '退出客服' == msg_text:
        that_row.on_service = False
        dbsession.commit()
        return ResponseMsg.text(msg, "您已退出智能客服系统")

    dbsession.commit()
    return customer_service_response(msg) if that_row.on_service else tuling_response(msg)


def __handle_event(msg):
    if msg['Event'] == 'subscribe':
        return "感谢关注南京大学智能数据决策工作室公众号！！"
    elif msg['Event'] == 'SCAN':
        return "您已成功再次关注…然而并没有什么用～"
    else:
        return ""
