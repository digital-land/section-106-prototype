# -*- coding: utf-8 -*-
import os
import json


if os.environ.get('VCAP_SERVICES') is not None:
    vcap_services = json.loads(os.environ.get('VCAP_SERVICES'))
    os.environ['SQLALCHEMY_DATABASE_URI'] = vcap_services['postgres'][0]['credentials']['uri']
    os.environ['SECRET_KEY'] = vcap_services['user-provided'][0]['credentials']['SECRET_KEY']


class Config:
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    JSON_SORT_KEYS = True


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    TESTING = True
