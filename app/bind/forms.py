# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask_wtf import FlaskForm as Form, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp


class RegisterForm(Form):
    phone_number = StringField(
        'Phone Number', validators=[
            DataRequired(), Regexp('^1[0-9]{10}$', message='必须为11位手机号码')
        ])
    submit = SubmitField("Get Verify Code")


class VerifyForm(Form):
    code = StringField(
        'Verify Code', validators=[
            DataRequired(), Regexp('^\d{4}$', message='请输入4位验证码')
        ])
    verify = SubmitField('Sign Up')


class StuidForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    validate_code = StringField('Validate Code', validators=[
        DataRequired(), Regexp('^[a-zA-Z0-9]{4}$', message='请输入4位验证码')])
    submit = SubmitField("Verify Login In")


class EmptyForm(Form):
    pass
