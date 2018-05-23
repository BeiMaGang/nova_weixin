# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from novamysql import engine
# from novamysql import create_engine
from .config import (config, DB_HOSTNAME, DB_PASSWORD,
                     DB_USERNAME, DB_NAME, DB_PORT)

bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    os.environ['config_flask'] = config_name

    if not os.path.exists('./log'):
        os.mkdir('./log')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        "mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8".format(
            user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOSTNAME,
            port=DB_PORT, database=DB_NAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    engine.init_app(app)
    engine.create_all(app=app)
    # create_engine(DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOSTNAME, DB_PORT)
    bootstrap.init_app(app)
    moment.init_app(app)

    from .bind import bind as bind_blueprint
    app.register_blueprint(bind_blueprint, url_prefix='/bind')
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .weixin import weixin as weixin_blueprint
    app.register_blueprint(weixin_blueprint)

    return app
