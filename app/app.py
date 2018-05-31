# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os
import json
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from packages.utils.sql import engine
from app.config import (config, DB_HOSTNAME, DB_PASSWORD, DB_USERNAME,
                        DB_NAME, DB_PORT, MENU, APP_ID, SECRET)
from packages.utils.wechatAccAPI import Url, Communicate, AccessToken
from packages.utils.log import NovaLog

logger = NovaLog("app_app")
bootstrap = Bootstrap()
moment = Moment()


def create_menu():
    token_ret = AccessToken.get(APP_ID, SECRET)
    if token_ret['status'] == 1:
        url = Url.create_menu.format(access_token=token_ret['access_token'])
        ret = Communicate.post(url, data=json.dumps(MENU, ensure_ascii=False).encode('utf-8'))
        if not ret['errcode']:
            return ret
    return None


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    os.environ['config_flask'] = config_name

    if not os.path.exists('./log'):
        os.mkdir('./log')
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        "mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8".format(
            user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOSTNAME,
            port=DB_PORT, database=DB_NAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    engine.init_app(app)
    engine.create_all(app=app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from .bind import bind as bind_blueprint
    app.register_blueprint(bind_blueprint, url_prefix='/bind')
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .weixin import weixin as weixin_blueprint
    app.register_blueprint(weixin_blueprint)
    return app
