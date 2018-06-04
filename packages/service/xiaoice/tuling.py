# -*- coding: utf-8 -*-
"""
Created by suun on 6/1/2018
"""
import requests
import json
from pprint import pprint
API_V2_URL = 'http://openapi.tuling123.com/openapi/api/v2'
ERROR_CORRESPONDENCE = {
    5000: '无解析结果',
    6000: '暂不支持该功能',
    4000: '请求参数格式错误',
    4001: '加密方式错误',
    4002: '无功能权限',
    4003: '该apikey没有可用请求次数',
    4005: '无功能权限',
    4007: 'apikey不合法',
    4100: 'userid获取失败',
    4200: '上传格式错误',
    4300: '批量操作超过限制',
    4400: '没有上传合法userid',
    4500: 'userid申请个数超过限制',
    4600: '输入内容为空',
    4602: '输入文本内容超长(上限150)',
    7002: '上传信息失败',
    8008: '服务器错误'
}


def tuling_reply(api_key, user_id, content):
    user_id = ''.join(filter(str.isalnum, user_id))
    params = {
        # 'reqType': 0,
        "perception": {
            "inputText": {
                "text": content
            },
            "selfInfo": {
                "location": {
                    "city": "南京",
                    "province": "江苏",
                    "street": "南京大学仙林校区"
                }
            }
        },
        "userInfo": {
            "apiKey": api_key,
            "userId": user_id
        }
    }
    api_reply = requests.post(API_V2_URL, data=json.dumps(params)).json()
    if len(api_reply['intent']) == 1 and\
            api_reply['intent']['code'] in ERROR_CORRESPONDENCE.keys():
        return {
            'status': 0,
            'errcode': api_reply['intent']['code'],
            'errmsg': ERROR_CORRESPONDENCE[api_reply['intent']['code']]
        }
    transform_reply = {}
    reply_results = api_reply['results']
    for line in reply_results:
        if line['resultType'] == 'news':
            details = []
            for idx, news in enumerate(line['values']['news']):
                details.append({
                    'title': news['name'],
                    'description': news['info'],
                    'picurl': 'http:' + news['icon'],
                    'url': news['detailurl']
                })
                if idx == 7:
                    break
            transform_reply['news'] = details
        elif line['resultType'] == 'text':
            transform_reply['text'] = line['values']['text']
        elif line['resultType'] == 'url':
            transform_reply['url'] = line['values']['url']
    if 'url' in transform_reply:
        transform_reply['text'] = __wrap_href(transform_reply['url'], transform_reply['text'])
        transform_reply.pop('url')
    return {
        'status': 1,
        'content': transform_reply
    }


def __wrap_href(url, content):
    return "<a href=\"%s\">%s</a>" % (url, content)


if __name__ == '__main__':
    pprint(tuling_reply('cea0705c45e3449eb3037953166962e0', '3123123', "我想看新闻"))
