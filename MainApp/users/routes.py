from flask import render_template,request,flash,redirect,url_for,abort,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc
from flask_mail import Message
from threading import Thread

from MainApp import  db, bcrypt, mail ,app
from MainApp.models import User, Posts
from MainApp.users.forms import LoginForm, SignUpForm

users = Blueprint('users',__name__)

@users.route('/signup',methods=['GET','POST'])
def signUpPage():
	if current_user.is_authenticated:
		return redirect(url_for('users.homePage'))
	form = SignUpForm(request.form)
	if request.method == "POST" and form.validate():
		username = form.username.data
		email = form.email.data
		password = form.password.data
		hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
		user = User(username=username, password=hashed_password, email=email)			
		db.session.add(user)
		db.session.commit()	
		thread = Thread(target=sendMail, args=(user,app,))
		thread.start()
		flash(f'Account Created for {username}')
		return redirect(url_for('users.loginPage'))

	return render_template('signup.html',form=form)


@users.route('/login',methods=['GET','POST'])
def loginPage():
	if current_user.is_authenticated:
		return redirect(url_for('main.homePage'))
	form = LoginForm(request.form)
	if request.method == "POST" and form.validate():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			if next_page:
				print(next_page) 
				return redirect(next_page) # will directly have the routes function name
			return redirect(url_for('main.homePage'))
		flash('Login Unsuccessful. Please Check the username and password','warning')

	return render_template('login.html',form=form)


@users.route('/logout',methods=['GET'])
@login_required
def logoutPage():
	if current_user.is_authenticated:
		logout_user()
		flash('Logout Successful','success')
	return redirect(url_for('users.loginPage'))


@users.route('/profile',methods=['GET'])
@login_required
def accountPage():
	page = request.args.get('page',1,type=int)
	posts = Posts.query.filter_by(user_id=current_user.id).order_by(desc(Posts.id)).paginate(per_page=5,page=page)
	return render_template('account.html',posts=posts)


@users.route('/profile/<string:username>',methods=['GET'])
@login_required
def anyProfilePage(username):
	user = User.query.filter_by(username=username).first()
	page = request.args.get('page',1,type=int)
	if user and page:
		posts = Posts.query.filter_by(author=user).order_by(desc(Posts.id)).paginate(per_page=5,page=page)
		return render_template('any_profile.html',posts=posts,username=username)
	abort(404,'Route Does Not Exists')



def sendMail(user,mail_app):
	msg = Message('Account Created at Blog Sharing Platform',sender='noreply@blog.com',recipients=[user.email])
	msg.body = f'''
			Hello, {user.username} we are glad that you created a account at Blog Sharing Platform.
			Start writing your blogs!!			
	'''
	with app.app_context():
		mail.send(msg)
	print('mail sent############')


# @app.route('/comment/new/<int:post_id>',methods=["GET","POST"])
# @login_required
# def newCommentPage(post_id):
# 	post = Posts.query.get(post_id)
# 	user_comment = request.form['comment']
# 	if request.method == 'POST' and post:
# 		comment = Comment(author=current_user, content=user_comment, post=post )
# 		db.session.add(comment)
# 		db.session.commit()
# 		return redirect(url_for('individualPostPage',post_id=post.id))
# 	else:
# 		abort(404,'Route Does Not Exists !')


# @app.route('/comment/delete/<int:post_id>/<int:comment_id>',methods=["GET","POST"])
# @login_required
# def deleteCommentPage(post_id,comment_id):
# 	post = Posts.query.get(post_id)
# 	user_comment = Comment.query.get(comment_id)
# 	if user_comment and post:
# 		if user_comment.author == current_user:
# 			db.session.delete(user_comment)
# 			db.session.commit()
# 			print("######deleted")
# 			return redirect(url_for('individualPostPage',post_id=post.id))
# 		else:
# 			abort(403,'UnAuthorized Access !')
# 	else:
# 		abort(404,'Route Does Not Exists !')