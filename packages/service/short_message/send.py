# -*- coding: utf-8 -*-
"""
Created by suun on 5/17/2018
"""
import base64
import datetime
import hmac
import json
import uuid
import urllib.parse
import requests
from app.config import SHORT_MESSAGE_ACCESS_ID, SHORT_MESSAGE_ACCESS_SECRET


def quote(text):
    return urllib.parse.quote(text, safe='~')


def stringify(**kwargs):
    pairs = []
    for k, v in sorted(kwargs.items()):
        pairs.append('{}={}'.format(k, v))
    return '&'.join(pairs)


def canonicalize(**kwargs):
    pairs = []
    for k, v in sorted(kwargs.items()):
        pair = '{}={}'.format(quote(k), quote(v))
        pairs.append(pair)
    return quote('&'.join(pairs))


def sign(text, secret):
    text = text.encode('utf-8')
    key = (secret + '&').encode('utf-8')
    digest = hmac.new(key, text, 'sha1').digest()
    signture = quote(base64.b64encode(digest))
    return signture


class AliSMS(object):

    # _defaults = [
    #     ('action', 'SendSms'),
    #     ('format', 'JSON'),
    #     ('region_id', 'cn-hangzhou'),
    #     ('signature_method', 'HMAC-SHA1'),
    #     ('signature_version', '1.0'),
    #     ('sms_version', '2017-05-25'),
    #     ('domain', 'https://dysmsapi.aliyuncs.com'),
    # ]

    def __init__(self, app_key, app_secret, sign_name):
        # for k, v in self._defaults:
        #     setattr(self, k, settings.get(k, v))
        self.action = 'SendSms'
        self.format = 'JSON'
        self.region_id = 'cn-hangzhou'
        self.signature_method = 'HMAC-SHA1'
        self.signature_version = '1.0'
        self.sms_version = '2017-05-25'
        self.domain = 'https://dysmsapi.aliyuncs.com'
        self.app_key = app_key
        self.app_secret = app_secret
        self.sign_name = sign_name

    def send(self, phone, template_code, template_params):
        body = self._create_body(phone, template_code, template_params)
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        res = requests.post(self.domain, data=body, headers=headers)
        return res

    def _create_body(self, phone, template_code, template_params):
        params = self._create_params(phone, template_code, template_params)
        text = 'POST&%2F&' + canonicalize(**params)
        signture = sign(text, self.app_secret)
        body = 'Signature={}&{}'.format(signture, stringify(**params))
        return body.encode('utf-8')

    def _create_params(self, phone, template_code, template_params):
        return {
            'AccessKeyId': self.app_key,
            'Action': self.action,
            'Format': self.format,
            'PhoneNumbers': phone,
            'RegionId': self.region_id,
            'SignName': self.sign_name,
            'SignatureMethod': self.signature_method,
            'SignatureNonce': str(uuid.uuid4()),
            'SignatureVersion': self.signature_version,
            'TemplateCode': template_code,
            'TemplateParam': json.dumps(template_params),
            'Timestamp': datetime.datetime.utcnow().isoformat("T"),
            'Version': self.sms_version,
        }


sms = AliSMS(SHORT_MESSAGE_ACCESS_ID, SHORT_MESSAGE_ACCESS_SECRET, "智能数据决策工作室")


def send_verify_code(phone_number, verify_code):
    params = {
        'code': verify_code
    }
    ret = sms.send(phone_number, "SMS_134327463", params).json()
    return 'Code' in ret and ret['Code'] == 'OK'

