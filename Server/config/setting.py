# -*- coding: utf-8 -*-
import os

# base setting
SERVERPORT = 8800

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# local setting
SQLALCHEMY_DATABASE_URI = 'sqlite:///lineup.sqlite3'    # 'sqlite:///root:Q123456@127.0.0.1/sqlite'
# SQLALCHEMY_DATABASE_URI = 'mysql:///root:Q123456@127.0.0.1/mysql'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUGE = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_ENCODING = "utf-8"

# production setting

UPLOAD_FOLDER = 'web'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
