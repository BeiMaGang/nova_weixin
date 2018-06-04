# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
import random
import time
from flask import (render_template, session, flash, request, url_for, redirect)
from app.bind import bind
from app.bind.forms import RegisterForm, VerifyForm, StuidForm
from packages.service.short_message import send_verify_code
from packages.utils.wechatAccAPI import get_openid_from_code
from app.config import APP_ID, SECRET
# from packages.commom.sql import PhoneBindForm, dbsession, StudentIdBindForm
from packages.utils import sql
from .middleware import get_base_img, verify_login, send_bind_template_msg


@bind.route('/', methods=['POST', 'GET'])
def default():
    code = request.args.get('code', None)
    if code is None:
        return redirect(url_for('bind.wrong_source'))
    if request.method == 'POST':
        if 'openid' not in session:
            session['openid'] = get_openid_from_code(code, appid=APP_ID, secret=SECRET)
            if not session['openid']:
                flash("获取 openid 出错。")
                return render_template('bind/bind.html')
        if 'in' in request.form:
            if len(sql.StudentIdBindForm.query.filter_by(openid=session['openid']).all()) > 0:
                return redirect(url_for('bind.redirect_rebind',
                                        target='bind.stuid_register'))
            return redirect(url_for('bind.stuid_register'))
        elif 'out' in request.form:
            if len(sql.PhoneBindForm.query.filter_by(openid=session['openid']).all()) > 0:
                return redirect(url_for('bind.redirect_rebind',
                                        target='bind.phone_register'))
            return redirect(url_for('bind.phone_register'))
        else:
            return render_template('error/404.html')
    return render_template('bind/bind.html')


@bind.route('/stuid_register', methods=['POST', 'GET'])
def stuid_register():
    if 'openid' not in session:
        return redirect(url_for('bind.wrong_source'))

    stuid_form = StuidForm()
    if stuid_form.validate_on_submit():
        username = stuid_form.username.data
        password = stuid_form.password.data
        validate_code = stuid_form.validate_code.data
        ret = verify_login(session['validate_code_cookies'], username, password, validate_code)
        if ret['status']:
            founds = sql.StudentIdBindForm.query.filter_by(openid=session['openid']).all()
            if len(founds) > 0:
                founds[0].username = username
                founds[0].password = password
            else:
                sql.dbsession.add(
                    sql.StudentIdBindForm(openid=session['openid'],
                                          username=username, password=password))
            sql.dbsession.commit()
            session.pop('validate_code_cookies')
            return redirect(url_for('bind.binded', username=username))
        else:
            flash(ret['errmsg'])
    session['validate_code_cookies'], img_stream = get_base_img()
    flash('您的密码仅用于此次验证，不会被保存。')
    return render_template('bind/stuid_register.html', img_stream=img_stream, form=stuid_form)


@bind.route('/phone_register', methods=['POST', 'GET'])
def phone_register():
    if 'openid' not in session:
        return redirect(url_for('bind.wrong_source'))

    register_form = RegisterForm()
    verify_form = VerifyForm()

    # 请求短信验证码
    if register_form.submit.data and register_form.validate_on_submit():
        input_number = ''.join(str(i) for i in random.sample(range(0, 9), 4))
        if 'time' in session and time.time() - session['time'] < 60:
            flash("请在 60 秒后再次请求发送短信验证码。")
        elif send_verify_code(register_form.phone_number.data, input_number):
            session['time'] = time.time()
            session['phone_number'] = register_form.phone_number.data
            session['verify_code'] = input_number
        else:
            flash("发送验证码出错，请稍后重试。")

    # 验证短信验证码
    elif verify_form.verify.data and verify_form.validate_on_submit():

        if 'verify_code' not in session:
            flash("您还未获取短信验证码。")
        elif str(verify_form.code.data) == session['verify_code']:

            founds = sql.PhoneBindForm.query.filter_by(openid=session['openid']).all()
            if len(founds) > 0:
                founds[0].phone_number = session['phone_number']
            else:
                sql.dbsession.add(sql.PhoneBindForm(phone_number=session['phone_number'],
                                                    openid=session['openid']))
            sql.dbsession.commit()

            session.pop('verify_code')
            session.pop('time')
            session.pop('phone_number')
            return redirect(url_for('bind.binded', username=session['phone_number']))
        else:
            flash("验证码错误。")

    return render_template('bind/phone_register.html',
                           register_form=register_form, verify_form=verify_form)


@bind.route('/binded')
def binded():
    print(session)
    if 'openid' not in session:
        return redirect(url_for('bind.wrong_source'))

    username = request.args.get('username', None)
    print(request.args)
    if username:
        send_bind_template_msg(appid=APP_ID, secret=SECRET,
                               account=username, touser=session['openid'])
    session.pop('openid')
    return render_template('commom/blank.html', title='Nova - Success', content='绑定成功。')


@bind.route('/wrong_source')
def wrong_source():
    return render_template('commom/blank.html', title='Nova - Error', content='请从微信打开此页面。')


@bind.route('/redirect_rebind')
def redirect_rebind():
    target = request.args.get('target', None)
    if not target:
        return redirect(url_for('weixin.error404'))
    params = {
        'success': {
            'href': url_for(target),
            'value': '继续'
        },
        'fail': {
            'href': url_for('bind.binded'),
            'value': '取消'
        }
    }
    flash('你已绑定过，请点击\"继续\"修改绑定信息。')
    return render_template('commom/redirect.html',
                           params=params)
