# -*- coding: utf-8 -*-
import os
import json


if os.environ.get('VCAP_SERVICES') is not None:
    vcap_services = json.loads(os.environ.get('VCAP_SERVICES'))
    os.environ['DATABASE_URL'] = vcap_services['postgres'][0]['credentials']['uri']
    os.environ['SECRET_KEY'] = vcap_services['user-provided'][0]['credentials']['SECRET_KEY']

class Config:
    CONFIG_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(CONFIG_ROOT, os.pardir))
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JSON_SORT_KEYS = True
    UPLOAD_FOLDER = '/tmp'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    BASE_SCHEMA_URL = 'https://raw.githubusercontent.com/digital-land/alpha-data/master/schema'


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    TESTING = True
