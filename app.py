from flask_sqlalchemy import SQLAlchemy
import os
from os import environ
from flask_migrate import Migrate
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c5723c7a0956175ca1e56086adc6bdc18064d2659be3b04fcd3bb89d1fbfe482'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///arctic_DB2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={
    'expire_on_commit': False
})

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
mail = Mail(app)

from commands import usersbp
app.register_blueprint(usersbp)

from authentication.routes import * 
from toestellen.routes import *
from kaarten.routes import *
from hours.routes import *

