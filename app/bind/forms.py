# -*- coding: utf-8 -*-
# Author: shizhenyu96@gamil.com
# github: https://github.com/imndszy
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
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
            DataRequired(), Regexp('^^\d{4}$', message='请输入4位验证码')
        ])
    verify = SubmitField('Sign Up')

# class BindForm(Form):
#     stuid = StringField('Student ID', validators=[DataRequired(),
#                                                   Regexp('^[0-9]*$', 0,
#                                                          'Student ID must have only numbers.')])
#     certification = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Log In')
