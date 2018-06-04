# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask_wtf import FlaskForm as Form, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp


class RegisterForm(Form):
    phone_number = StringField(
        '手机号码', validators=[
            DataRequired(), Regexp('^1[0-9]{10}$', message='必须为11位手机号码')
        ])
    submit = SubmitField("获取短信验证码")


class VerifyForm(Form):
    code = StringField(
        '短信验证码', validators=[
            DataRequired(), Regexp('^\d{4}$', message='请输入4位短信验证码')
        ])
    verify = SubmitField('注册')


class StuidForm(Form):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    validate_code = StringField('验证码', validators=[
        DataRequired(), Regexp('^[a-zA-Z0-9]{4}$', message='请输入4位验证码')])
    submit = SubmitField("绑定用户")
