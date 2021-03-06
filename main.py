from flask import Flask
from flaskext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
from flask_wtf import CsrfProtect

import gocardless
import stripe

import logging
import logger

logging.basicConfig(level=logging.NOTSET)

app = Flask(__name__)
csrf = CsrfProtect(app)
app.config.from_envvar('SETTINGS_FILE')

logger.setup_logging(app)

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()

assets = Environment(app)
css = Bundle('css/main.css',
                output='gen/packed.css', filters='cssmin')
assets.register('css_all', css)

gocardless.environment = app.config['GOCARDLESS_ENVIRONMENT']
gocardless.set_details(app_id=app.config['GOCARDLESS_APP_ID'],
                        app_secret=app.config['GOCARDLESS_APP_SECRET'],
                        access_token=app.config['GOCARDLESS_ACCESS_TOKEN'],
                        merchant_id=app.config['GOCARDLESS_MERCHANT_ID'])

stripe.api_key = app.config['STRIPE_SECRET_KEY']


def external_url(endpoint, **values):
    """ Generate an absolute external URL. url_for(_external=True) doesn't seem to work
        if we're behind a proxy as in production """
    return app.config.get('BASE_URL', 'https://www.emfcamp.org') + url_for(endpoint, **values)

from views import *
from models import *

if __name__ == "__main__":
    if app.config.get('DEBUG'):
        db.create_all()

    app.run()
