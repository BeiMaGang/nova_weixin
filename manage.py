# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os
from app import create_app, create_menu

# default及development环境下并不会真正发送模板消息

# print("create menu status: %s" % create_menu())
app = create_app(os.getenv('FLASK_CONFIG') or 'production')

if __name__ == "__main__":
    app.run(port=8881, debug=True)
