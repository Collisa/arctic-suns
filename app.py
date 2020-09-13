from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_migrate import Migrate
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c5723c7a0956175ca1e56086adc6bdc18064d2659be3b04fcd3bb89d1fbfe482'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///arctic_DB2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from commands import usersbp
app.register_blueprint(usersbp)

from authentication.routes import * 
from toestellen.routes import *
from kaarten.routes import *

