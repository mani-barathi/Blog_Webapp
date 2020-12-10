from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt   			# pip install --no-use-pep517 flask-bcrypt
from flask_login import LoginManager        # pip install flask-login
from flask_mail import Mail
from flask_cors import CORS 				# pip install flask-cors

from MainApp.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.loginPage'



app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app) 
bcrypt.init_app(app) 
login_manager.init_app(app)
mail.init_app(app)


from MainApp.users.routes import users
from MainApp.posts.routes import posts
from MainApp.main.routes import main
from MainApp.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)

