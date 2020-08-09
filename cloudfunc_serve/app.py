# coding=utf-8

import logging
import os
from os.path import join

from flask_sqlalchemy import SQLAlchemy

log = logging.getLogger(__name__)

db = SQLAlchemy()


def make_settings(app, settings):
    """
    This function is invoked before initializing app.
    """
    settings['data_dir'] = join(settings['home'], 'data')
    os.makedirs(settings['data_dir'], exist_ok=True)


def init_app(app, settings):
    """
    This function is invoked before running app.
    """
    _init_sqlalchemy(app, settings)


def _init_sqlalchemy(app, settings):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
