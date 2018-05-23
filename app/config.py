# -*- coding: utf-8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os
import sys

from app.my_config import DB_NAME, DB_PASSWORD, DB_USERNAME, DB_HOSTNAME, DB_PORT, ROOT_USER, \
    USER_EMAIL, USER_PASSWD, ADDRESS, OR_SECRET_KEY, APP_ID, SECRET, TEMPLATE_ID, TOKEN,\
    ACCESS_KEY_ID, ACCESS_KEY_SECRET

basedir = os.path.abspath(os.path.dirname(__file__))

PY2 = sys.version_info[0] == 2


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or OR_SECRET_KEY

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

MENU = {
    "button": [
        {
            "name": "通知消息",
            "sub_button": [
                {
                    "type": "click",
                    "name": "未读消息",
                    "key": "not_read_mes"
                },
                {
                    "type": "view",
                    "name": "历史消息",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s"
                           "&redirect_uri=%s/history&response_type=code&scope=snsapi_base"
                           "&state=123&connect_redirect=1#wechat_redirect"
                           % (APP_ID, ADDRESS)
                }
                # ,
                # {
                #     "type": "click",
                #     "name": "近期消息",
                #     "key": "recent_mes"
                # }
            ]

        },
        {
            "name": "个性服务",
            "sub_button": [
                {
                    "type": "view",
                    "name": "微信问问（校内）",
                    "url": "http://smeug.nju.edu.cn/q2a/index.php"
                },
                {
                    "type": "view",
                    "name": "校外用户绑定",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&"
                           "redirect_uri={url}&response_type=code&scope=snsapi_base"
                           "#wechat_redirect".format(
                                                     appid=APP_ID,
                                                     url="http://weixin.njunova.com/"
                                                         "bind/phone_register"
                           )
                },
                {
                    "type": "view",
                    "name": "主页",
                    "url": "http://weixin.njunova.com"
                }
            ]

        }

        # {
        #     "name": "个人查询",
        #     "sub_button": [
        #         {
        #             "type": "click",
        #             "name": "日常考核",
        #             "key": "daily_assess"
        #         },
        #         {
        #             "type": "click",
        #             "name": "绩点查询",
        #             "key": "gpa"
        #         },
        #         {
        #             "type": "click",
        #             "name": "推免查询",
        #             "key": "recom"
        #         },
        #         {
        #             "type": "click",
        #             "name": "导师查询",
        #             "key": "tutor"
        #         }
        #     ]
        # },
    ]
}
