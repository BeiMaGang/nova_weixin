# -*- coding: utf-8 -*-
"""
Created by suun on 5/10/2018
"""
from flask_sqlalchemy import SQLAlchemy

engine = SQLAlchemy()

from novamysql.models import *

dbsession = engine.session

