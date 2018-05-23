# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask import (render_template, redirect, url_for, session, flash, request)
import random
import time
from nova_weixin.app.bind import bind
from nova_weixin.app.bind.forms import RegisterForm, VerifyForm
from sms import send_verify_code
from wechatAccAPI import get_openid_from_code
from app.config import APP_ID, SECRET
from novamysql import PhoneBindForm, dbsession


@bind.route('/')
def default():
    print("what")
    return render_template('500.html')


@bind.route('/phone_register', methods=['POST', 'GET'])
def phone_register():
    # if 'openid' in session:
    #     return redirect(url_for("bind.rebind"))
    #
    code = request.args.get('code', None)
    if code is None:
        return render_template('wrong_src.html')
    #
    register_form = RegisterForm()
    verify_form = VerifyForm()
    if register_form.submit.data and register_form.validate_on_submit():
        input_number = ''.join(str(i) for i in random.sample(range(0, 9), 4))
        # if 'time' in session and time.time() - session['time'] < 60:
        #     flash("Please resend verify code 60 seconds later")
        # else:
        session['time'] = time.time()
        session['phone_number'] = register_form.phone_number.data
        session['verify_code'] = input_number
        print(send_verify_code(register_form.phone_number.data, input_number))

    elif verify_form.verify.data and verify_form.validate_on_submit():

        if 'verify_code' not in session:
            flash("You have not got verify code")
        elif str(verify_form.code.data) == session['verify_code']:
            if 'openid' not in session:
                openid = get_openid_from_code(code, APP_ID, SECRET)
                session['openid'] = openid
            else:
                openid = session['openid']
            founds = PhoneBindForm.query.filter_by(openid=openid).all()
            if len(founds) > 0:
                founds[0].phone_number = session['phone_number']
            else:
                dbsession.add(PhoneBindForm(phone_number=session['phone_number'], openid=openid))
            dbsession.commit()
            print(session)
            return render_template('bind/binded.html')
        else:
            flash("Your verify code is wrong")

    return render_template('bind/phone_register.html',
                           register_form=register_form, verify_form=verify_form)


@bind.route('/rebind')
def rebind():
    return render_template("500.html")

# @bind.route('/register', methods=['GET', 'POST'])
# def register():
#     form = BindForm()
#     if form.validate_on_submit():
#         stuid = form.stuid.data
#         passwd = form.certification.data
#         session['stuid'] = stuid
#         session['passwd'] = passwd
#         session['register'] = True
#         # print(session)
#         # verify_status = verify_password(stuid, passwd)
#         # if verify_status and verify_status != -1:
#         #     session['register'] = True
#         #     query_result = get_openid(stuid)
#         #     if query_result:                                      #该学号已经绑定微信号
#         #         openid = query_result.encode('utf8')
#         #         session['openid'] = openid
#         #         return redirect(url_for('bind.rebind'))
#         #     else:
#         #         if save_new_student(stuid) == -1:
#         #             return "注册失败，请联系管理员！"
#         #         return redirect(url_for('bind.get_qrcode'))
#         # elif verify_status == -1:
#         #     return render_template('404.html')
#         # else:
#         #     flash('Invalid Student ID or Password.')
#         return redirect(url_for('bind.get_qrcode'))
#         # return render_template('404.html')
#     return render_template('bind/phone_register.html', form=form)


# @bind.route('/qrcode', methods=['GET', 'POST'])
# def get_qrcode():
#     if session.get('register'):
#         # print("line 49")
#         acc_token = get_token(appid=APP_ID, appsecret=SECRET)
#         ticket = create_ticket("QR_SCENE", acc_token=acc_token.get('acc_token'),
#                                scene_id=int(session['stuid']))
#         url = get_qrcode_url(ticket)
#         return redirect(url)
#     return render_template('404.html')

# @bind.route('/rebind', methods=['GET', 'POST'])
# def rebind():
#     # if session.get('register') and session.get('openid'):
#     if session.get('register'):
#         form = ReBindForm()
#         if form.validate_on_submit():
#             coverage = form.coverage.data
#             if coverage == 'yes':
#                 acc_token = get_token(appid=APP_ID, appsecret=SECRET)
#                 ticket = create_ticket("QR_SCENE", acc_token=acc_token.get('acc_token'),
#                                        scene_id=int(session['stuid']))
#                 if ticket['status'] == 1:
#                     url = get_qrcode_url(ticket['ticket'])
#                     return redirect(url)
#                 else:
#                     return ticket['errmsg']
#             else:
#                 return redirect(url_for('main.index'))
#         return render_template('bind/rebind.html', form=form)
#     return render_template('404.html')
