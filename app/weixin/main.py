# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import hashlib
import xml.etree.ElementTree as ET

from flask import request, make_response, render_template, redirect, url_for

from app.weixin import weixin
from app.config import TOKEN
from .entrance import handle_msg


@weixin.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error/404.html'), 404


def parse(rec):
    """
    :param rec: rec is a xml file
    :return: return a dictionary
    """
    root = ET.fromstring(rec)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg


def verification():
    """
    verify the weixin token
    """
    token = TOKEN
    data = request.args
    signature = data.get('signature', '')
    timestamp = data.get('timestamp', '')
    nonce = data.get('nonce', '')
    s = [timestamp, nonce, token]
    s.sort()
    s = ''.join(s)
    if hashlib.sha1(s.encode('utf8')).hexdigest() == signature:
        return 1
    return 0


@weixin.route('/', methods=['GET'])
def wechat_auth():
    echostr = request.args.get('echostr', '')
    if verification():
        return make_response(echostr)
    return render_template("index.html")
    # return redirect(url_for('.index'))


@weixin.route('/', methods=['POST'])
def wechat_msg():
    rec = request.data
    if rec:
        msg = parse(rec)
        return handle_msg(msg)


@weixin.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
