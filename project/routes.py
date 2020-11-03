from flask import render_template,request,flash,redirect,url_for,abort
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc
from . import app, db, bcrypt
from .models import User, Posts, Comment
from .forms import LoginForm, SignUpForm, PostForm

@app.route('/',methods=['GET','POST'])
def homePage():
	posts = []
	if current_user.is_authenticated:
		page = request.args.get('page',1,type=int)
		posts = Posts.query.order_by(desc(Posts.id)).paginate(per_page=5,page=page)
	return render_template('index.html',posts=posts)


@app.route('/signup',methods=['GET','POST'])
def signUpPage():
	if current_user.is_authenticated:
		return redirect(url_for('homePage'))
	form = SignUpForm(request.form)
	if request.method == "POST" and form.validate():
		username = form.username.data
		email = form.email.data
		password = form.password.data
		hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
		user = User(username=username, password=hashed_password, email=email)			
		db.session.add(user)
		db.session.commit()	
		flash(f'Account Created for {username}')
		return redirect(url_for('loginPage'))

	return render_template('signup.html',form=form)


@app.route('/login',methods=['GET','POST'])
def loginPage():
	if current_user.is_authenticated:
		return redirect(url_for('homePage'))
	form = LoginForm(request.form)
	if request.method == "POST" and form.validate():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			if next_page:
				print(next_page) 
				return redirect(next_page) # will directly have the 
			return redirect(url_for('homePage'))
		flash('Login Unsuccessful. Please Check the username and password','warning')

	return render_template('login.html',form=form)


@app.route('/logout',methods=['GET'])
@login_required
def logoutPage():
	if current_user.is_authenticated:
		logout_user()
		flash('Logout Successful','success')
	return redirect(url_for('loginPage'))


@app.route('/account',methods=['GET'])
@login_required
def accountPage():
	page = request.args.get('page',1,type=int)
	posts = Posts.query.filter_by(user_id=current_user.id).order_by(desc(Posts.id)).paginate(per_page=5,page=page)
	return render_template('account.html',posts=posts)


@app.route('/profile/<string:username>',methods=['GET'])
@login_required
def anyProfilePage(username):
	user = User.query.filter_by(username=username).first()
	if user:
		page = request.args.get('page',1,type=int)
		posts = Posts.query.filter_by(author=user).order_by(desc(Posts.id)).paginate(per_page=5,page=page)
		return render_template('any_profile.html',posts=posts,username=username)
	return abort(404,'Route Does Not Exists')


@app.route('/post/<int:post_id>',methods=['GET'])
@login_required
def individualPostPage(post_id):
	post = Posts.query.get(post_id)
	if post :
		return render_template('individual_post.html',post = post)
	return abort(404,'Route Does Not Exists')


@app.route('/post/new',methods=["GET","POST"])
@login_required
def newPostPage():
	form = PostForm(request.form)
	if request.method == 'POST' and form.validate():
		title = form.title.data
		content = form.content.data
		print(content)
		post = Posts(author = current_user, title = title, content=content )
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('homePage'))
	return render_template('post.html', form=form, act='New')


@app.route('/post/delete/<int:post_id>',methods=["GET","POST"])
@login_required
def deletePostPage(post_id):
	post = Posts.query.get(post_id)
	if post :
		is_user_authenticated_post = post.user_id == current_user.id
		if is_user_authenticated_post:
			db.session.delete(post)
			db.session.commit()
			flash('Post deleted Successfully !','success')
			return redirect(url_for('accountPage'))
		else:
			abort(403,'UnAuthorized Access !')
	else:
		abort(404,'Route Does Not Exists')


@app.route('/post/update/<int:post_id>',methods=["GET","POST"])
@login_required
def updatePostPage(post_id):
	post = Posts.query.get(post_id)
	form = PostForm(request.form)

	if post:
		is_user_authenticated_post = post.user_id == current_user.id
		if request.method == 'POST' and form.validate() and is_user_authenticated_post:
			post.title = form.title.data
			post.content = form.content.data
			db.session.commit()
			print("updated")
			return redirect(url_for('accountPage'))
		
		if is_user_authenticated_post:
			form = PostForm(title=post.title, content=post.content)
		return render_template('post.html', form=form,act='Edit')
	
	else:
		abort(404,'Route Does Not Exists !')


@app.route('/comment/new/<int:post_id>',methods=["GET","POST"])
@login_required
def newCommentPage(post_id):
	post = Posts.query.get(post_id)
	user_comment = request.form['comment']
	if request.method == 'POST' and post:
		comment = Comment(author=current_user, content=user_comment, post=post )
		db.session.add(comment)
		db.session.commit()
		return redirect(url_for('individualPostPage',post_id=post.id))
	else:
		abort(404,'Route Does Not Exists !')


@app.route('/comment/delete/<int:post_id><int:comment_id>',methods=["GET","POST"])
@login_required
def deleteCommentPage(post_id,comment_id):
	post = Posts.query.get(post_id)
	user_comment = Comment.query.get(comment_id)
	if user_comment and post:
		if user_comment.author == current_user:
			db.session.delete(user_comment)
			db.session.commit()
			return redirect(url_for('individualPostPage',post_id=post.id))
		else:
			abort(403,'UnAuthorized Access !')
	else:
		abort(404,'Route Does Not Exists !')