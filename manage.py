# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import nova_weixin.menu

# default及development环境下并不会真正发送模板消息
assert nova_weixin.menu.create_menu() != -1
app = nova_weixin.app.create_app(os.getenv('FLASK_CONFIG') or 'production')

if __name__ == "__main__":
    app.run(port=8881, debug=True)
