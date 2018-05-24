# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os
import sys
import menu
from app import create_app

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# default及development环境下并不会真正发送模板消息
assert menu.create_menu() != -1
app = create_app(os.getenv('FLASK_CONFIG') or 'production')

if __name__ == "__main__":
    app.run(port=8881, debug=True)
