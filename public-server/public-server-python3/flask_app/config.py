"""This module has configurations for flask app."""

import os
import sys
import logging
from logging import handlers
from flask import Flask
from flask_cors import CORS
from .utils.encode import MyFlaskJSONEncoder

app = Flask(__name__)

HOSTNAME = '0.0.0.0'
PORT = 8081
REDIS_HOST = 'database'
REDIS_PORT = 6379
OIDC_METADATA_URL = 'https://idp.wzstarter.org/dex/.well-known/openid-configuration'
OIDC_CLIENT_ID = 'APP-WZSTARTER-ORG'
OIDC_CLIENT_SECRET = 'ZXhhbXBsZS1hcHAtc2VjcmV0'
OIDC_DEFAULT_SCOPE = 'openid'
OIDC_DEFAULT_REDIRECT_URI = 'https://app.wzstarter.org/'

CONFIG = {
    "development": "flask_app.config.DevelopmentConfig",
    "testing": "flask_app.config.TestingConfig",
    "production": "flask_app.config.ProductionConfig",
    "default": "flask_app.config.ProductionConfig"
}


class BaseConfig(object):
    """Base class for default set of configs."""

    DEBUG = False
    TESTING = False
    LOGGING_FORMAT = "[%(asctime)s] [%(funcName)-30s] +\
                                    [%(levelname)-6s] %(message)s"
    LOGGING_LOCATION = 'web.log'
    LOGGING_LEVEL = logging.INFO
    CACHE_TYPE = 'simple'
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml',
                          'application/json', 'application/javascript']

    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500


class DevelopmentConfig(BaseConfig):
    """Default set of configurations for development mode."""

    DEBUG = True
    TESTING = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))


class ProductionConfig(BaseConfig):
    """Default set of configurations for prod mode."""

    DEBUG = False
    TESTING = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))


class TestingConfig(BaseConfig):
    """Default set of configurations for test mode."""

    DEBUG = False
    TESTING = True
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

def setup_logger():
    """Setup the logger with predefined formatting of time and rollup."""
    # generated_files = 'log_output'
    # logfile_name = '{0}/web.log'.format(generated_files)
    # if not os.path.exists(generated_files):
    #     os.makedirs(generated_files)

    logging.getLogger('').setLevel(logging.INFO)
    # handler = logging.handlers.RotatingFileHandler(logfile_name,
    #                                               maxBytes=10000000,
    #                                               backupCount=1000)

    handler = logging.StreamHandler(sys.stdout)

    LOGGING_FORMAT = "[%(asctime)s] [%(name)s.%(funcName)-30s]" +\
        "[%(levelname)-6s] %(message)s"
    datefmt = '%Y-%m-%d %H:%M:%S'
    handler.setFormatter(logging.Formatter(LOGGING_FORMAT, datefmt=datefmt))
    logging.getLogger('').addHandler(handler)

    # print('Logging into {}'.format(logfile_name))
    print('Logging into stdout')


def configure_app(app):
    """Configure the app w.r.t Flask-security, databases, loggers."""
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(CONFIG[config_name])

    setup_logger()
    
    # set up cross origin handling
    CORS(app, headers=['Content-Type'])

    app.json_encoder = MyFlaskJSONEncoder
    app.redis_config = RedisConfig()
    app.oidc_config = OIDCConfig()
    print("configure_app done")

class RedisConfig(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.hostname = host
        self.port = port

class OIDCConfig(object):
    def __init__(self, metadata_url=OIDC_METADATA_URL, client_id=OIDC_CLIENT_ID, client_secret=OIDC_CLIENT_SECRET, default_scope=OIDC_DEFAULT_SCOPE, default_redirect_uri=OIDC_DEFAULT_REDIRECT_URI):
        self.metadata_url = metadata_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.default_scope = default_scope
        self.default_redirect_uri = default_redirect_uri