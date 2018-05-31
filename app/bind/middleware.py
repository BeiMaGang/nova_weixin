# -*- coding: utf-8 -*-
"""
Created by suun on 5/29/2018
"""
import base64
import requests
from PIL import Image
from io import BytesIO

request_header = {
    'Host': 'cer.nju.edu.cn',
    'Origin': 'http://cer.nju.edu.cn',
    'Referer': 'http://cer.nju.edu.cn/amserver/UI/login',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}


def get_base_img():
    response = requests.get('http://cer.nju.edu.cn/amserver/verify/image.jsp',
                            headers=request_header)
    img_stream = base64.b64encode(response.content).decode()
    return dict(response.cookies), img_stream


def verify_login(cookies, username, password, validate_code):
    url = 'http://cer.nju.edu.cn/amserver/UI/Login'
    form_data = {
        'encoded': 'false',
        'goto': '',
        'gotoOnFail': '',
        'IDToken0': '',
        'IDButton': 'Submit',
        'IDToken1': username,
        'IDToken2': password,
        'inputCode': validate_code,
        'gx_charset': 'UTF-8'
    }
    plain_text = requests.post(url, data=form_data, headers=request_header, cookies=cookies).text
    if plain_text.count('验证码错误') == 2:
        return {'status': 0, 'errmsg': 'validate code is wrong.'}
    elif plain_text.count('用户名或密码错误') == 2:
        return {'status': 0, 'errmsg': 'username or password is wrong.'}
    elif '/imp/authLogin.do' in plain_text:
        return {'status': 1}
    else:
        return {'status': 0, 'errmsg': 'error that not handled occurs.'}
