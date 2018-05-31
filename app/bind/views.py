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
from .middleware import get_base_img, verify_login


@bind.route('/', methods=['POST', 'GET'])
def default():
    code = request.args.get('code', None)
    if code is None:
        return redirect(url_for('bind.wrong_source'))
    if request.method == 'POST':
        if 'openid' not in session:
            session['openid'] = get_openid_from_code(code, appid=APP_ID, secret=SECRET)
            if not session['openid']:
                flash("Error occurs while getting openid.")
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
                sql.dbsession.add(sql.StudentIdBindForm(openid=session['openid'],
                                                        username=username,
                                                        password=password))
            sql.dbsession.commit()
            session.pop('validate_code_cookies')
            return render_template('bind/binded.html')
        else:
            flash(ret['errmsg'])
    session['validate_code_cookies'], img_stream = get_base_img()
    return render_template('bind/stuid_register.html', img_stream=img_stream, form=stuid_form)


@bind.route('/phone_register', methods=['POST', 'GET'])
def phone_register():
    if 'openid' not in session:
        return redirect(url_for('bind.wrong_source'))

    register_form = RegisterForm()
    verify_form = VerifyForm()
    if register_form.submit.data and register_form.validate_on_submit():
        input_number = ''.join(str(i) for i in random.sample(range(0, 9), 4))
        if 'time' in session and time.time() - session['time'] < 60:
            flash("Please resend verify code 60 seconds later")
        elif send_verify_code(register_form.phone_number.data, input_number):
            session['time'] = time.time()
            session['phone_number'] = register_form.phone_number.data
            session['verify_code'] = input_number
        else:
            flash("Error occurs when sending verify code, try again later")

    elif verify_form.verify.data and verify_form.validate_on_submit():

        if 'verify_code' not in session:
            flash("You have not got verify code")
        elif str(verify_form.code.data) == session['verify_code']:
            founds = sql.PhoneBindForm.query.filter_by(openid=session['openid']).all()
            if len(founds) > 0:
                founds[0].phone_number = session['phone_number']
            else:
                sql.dbsession.add(sql.PhoneBindForm(phone_number=session['phone_number'],
                                                    openid=session['openid']))
            sql.dbsession.commit()
            session.pop('verify_code')
            return render_template('bind/binded.html')
        else:
            flash("Your verify code is wrong")

    return render_template('bind/phone_register.html',
                           register_form=register_form, verify_form=verify_form)


@bind.route('/wrong_source')
def wrong_source():
    return render_template('commom/blank.html', title='Error', content='请从微信打开此页面。')


@bind.route('/redirect_rebind')
def redirect_rebind():
    target = request.args.get('target', None)
    if not target:
        return redirect(url_for('weixin.error404'))
    params = {
        'success': {
            'href': url_for(target),
            'value': 'Confirm'
        },
        'fail': {
            'href': url_for('bind.default'),
            'value': 'Cancel'
        }
    }
    flash('You have bind before, click confirm to continue')
    return render_template('commom/redirect.html',
                           params=params)
