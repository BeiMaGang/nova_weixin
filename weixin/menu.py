# -*- coding:utf8 -*- 
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import json
import urllib2
from nova_weixin.config import MENU
import get_acc_token


def create_menu():
    acc_token = get_acc_token.get_token()
    if acc_token:
        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % acc_token
        data = MENU
        request = urllib2.urlopen(url, json.dumps(data, ensure_ascii=False))
        return json.loads(request.read())
    else:
        return "failed to get access_token!--menu.py"


if __name__ == "__main__":
    #create_menu()
    print "menu test"