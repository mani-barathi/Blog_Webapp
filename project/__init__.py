from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt   			# pip install --no-use-pep517 flask-bcrypt
from flask_login import LoginManager        # pip install flask-login

app = Flask(__name__)
app.secret_key = 'Thisisasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'loginPage'

from . import routes