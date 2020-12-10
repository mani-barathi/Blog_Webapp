import os

class Config:
	SECRET_KEY = 'Thisisasecret'
	# change the database URI in production 
	SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = '587'
	MAIL_USE_TLS = True

	# store your email ID and Password in environment password
	MAIL_USERNAME = os.environ.get('EMAIL_ID')			
	MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
