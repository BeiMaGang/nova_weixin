# -*- coding: utf-8 -*-
"""
Created by suun on 5/31/2018
"""
from flask import render_template
from app.weixin import weixin

# errors


@weixin.route('/404')
def error404():
    return render_template('commom/blank.html', title='Error', content='Not Found')


@weixin.route('/403')
def error403():
    return render_template('commom/blank.html', title='Error', content='Forbidden')


@weixin.route('/410')
def error410():
    return render_template('commom/blank.html', title='Error', content='Gone')


@weixin.route('/500')
def error500():
    return render_template('commom/blank.html', title='Error', content='Interval Server Error')


@weixin.app_errorhandler(404)
def handle404(e):
    return render_template('commom/blank.html', title='Error', content='Not Found'), 404


@weixin.app_errorhandler(403)
def handle403(e):
    return render_template('commom/blank.html', title='Error', content='Forbidden'), 403


@weixin.app_errorhandler(410)
def handle410(e):
    return render_template('commom/blank.html', title='Error', content='Gone'), 410


@weixin.app_errorhandler(500)
def handle500(e):
    return render_template('commom/blank.html', title='Error', content='Interval Server Error'), 500

