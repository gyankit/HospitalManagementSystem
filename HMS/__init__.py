from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schema.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'main.login'
login_manager.login_message = f'Login required to excess this page'
login_manager.login_message_category = 'warning'

from HMS.main import main
from HMS.patient import patient
from HMS.diagnostic import diagnostic
from HMS.pharmacist import pharmacist

app.register_blueprint(main)
app.register_blueprint(patient)
app.register_blueprint(diagnostic)
app.register_blueprint(pharmacist)

from HMS import handlers
from HMS import models
login_manager._user_callback = models.load_user
