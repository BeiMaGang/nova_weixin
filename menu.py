# -*- coding: utf-8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
"""
该文件放在最外面文件夹中是为了方便更新微信自定义菜单
"""
import json
import sys

from app.config import PY2

if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

from app.config import MENU, APP_ID, SECRET
from packages.nova_wxsdk import WxApiUrl, CommunicateWithApi, get_token


def create_menu():
    acc_token = get_token(appid=APP_ID, appsecret=SECRET)
    if acc_token['status'] == 1:
        url = WxApiUrl.create_menu.format(access_token=acc_token['acc_token'])
        data = MENU
        return CommunicateWithApi.post_data(url, data=json.dumps(data, ensure_ascii=False).encode(
            'utf8'))
    else:
        return -1


if __name__ == "__main__":
    print(create_menu())
