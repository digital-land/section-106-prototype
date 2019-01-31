# -*- coding: utf-8 -*-
import os
import json


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
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    TESTING = True
