# -*- coding: utf-8 -*-
"""
Created by suun on 5/10/2018
"""

from packages.utils.sql import engine


class PhoneBindForm(engine.Model):
    __tablename__ = 'bind_phone'
    openid = engine.Column(engine.String(30), primary_key=True)
    phone_number = engine.Column(engine.String(11))


class StudentIdBindForm(engine.Model):
    __tablename__ = 'bind_stuid'
    openid = engine.Column(engine.String(30), primary_key=True)
    username = engine.Column(engine.String(20))
    password = engine.Column(engine.String(40))


class ServiceStatusForm(engine.Model):
    __tablename__ = 'service_status'
    openid = engine.Column(engine.String(30), primary_key=True)
    on_service = engine.Column(engine.Boolean)
