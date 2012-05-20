from flask import Flask
from flaskext.login import LoginManager
from flaskext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
app.config.from_envvar('SETTINGS_FILE')

login_manager = LoginManager()
login_manager.setup_app(app, add_context_processor=True)

db = SQLAlchemy(app)

mail = Mail(app)

assets = Environment(app)
css = Bundle('css/main.css', output='gen/packed.css')
assets.register('css_all', css)

import gocardless

gocardless.environment = app.config['GOCARDLESS_ENVIRONMENT']
gocardless.set_details(app_id=app.config['GOCARDLESS_APP_ID'],
                        app_secret=app.config['GOCARDLESS_APP_SECRET'],
                        access_token=app.config['GOCARDLESS_ACCESS_TOKEN'],
                        merchant_id=app.config['GOCARDLESS_MERCHANT_ID'])

from views import *
from models import *
db.create_all()

try:
    Prepay = TicketType.query.filter_by(name='Prepay Camp Ticket').one()
except NoResultFound, e:
    Prepay = TicketType('Prepay Camp Ticket', 250, 4, 30.00)
    db.session.add(Prepay)
    db.session.commit()

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

if __name__ == "__main__":
    app.run()
