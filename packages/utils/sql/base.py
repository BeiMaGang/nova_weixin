# -*- coding: utf-8 -*-
"""
Created by suun on 5/10/2018
"""
from flask_sqlalchemy import SQLAlchemy

engine = SQLAlchemy()

dbsession = engine.session

