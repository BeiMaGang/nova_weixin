# -*- coding: utf-8 -*-
"""
Created by suun on 5/10/2018
"""

from novamysql.base import engine


class PhoneBindForm(engine.Model):
    __tablename__ = 'phone_bind'
    openid = engine.Column(engine.String(30), primary_key=True)
    phone_number = engine.Column(engine.String(11))


class ServiceStatusForm(engine.Model):
    __tablename__ = 'service_status'
    openid = engine.Column(engine.String(30), primary_key=True)
    on_service = engine.Column(engine.Boolean)
