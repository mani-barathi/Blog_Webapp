from flask_login import UserMixin
from datetime import datetime
from . import db,app, login_manager

# This will load the User the session
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


# UserMixin has certain attributes and methods is_authenticated, is_active, is_annonymous, get_id
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(50), nullable=False)
	# not a column just a back reference to get all the posts of a single user
	# since backref is set as author , post.author will return the reference to user object
	posts = db.relationship('Posts',backref='author',lazy=True)
	comments = db.relationship('Comment',backref='author',lazy=True)

	def __repr__(self):
		return f'{self.id} --> {self.username}'

class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
	title = db.Column(db.String(50), unique=True, nullable=False)
	content = db.Column(db.Text, nullable=False)	
	# Foreign Key
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	#back reference to COmments
	comments = db.relationship('Comment',backref='post',lazy=True)

	def __repr__(self):
		return f'Post: {self.id} --> {self.date_posted}'

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	post_id = db.Column(db.Integer,db.ForeignKey('posts.id'),nullable=False)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

# TABLES are created with the lowercase name of Model Names