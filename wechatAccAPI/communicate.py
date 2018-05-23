# -*- coding: utf-8 -*-
"""
Created by suun on 5/14/2018
"""

import requests


class Communicate(object):
    @staticmethod
    def get(url, **kwargs):
        return requests.get(url, **kwargs).json()

    @staticmethod
    def post(url, data=None, **kwargs):
        return requests.post(url, data, **kwargs).json()
