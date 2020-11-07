from flask import render_template,request,flash,redirect,url_for,abort,jsonify,Blueprint
from flask_login import current_user, login_required
from sqlalchemy import desc
from MainApp import db, bcrypt
from MainApp.models import User, Posts, Comment
from MainApp.posts.forms import PostForm

posts = Blueprint('posts',__name__)


@posts.route('/post/<int:post_id>',methods=['GET'])
@login_required
def individualPostPage(post_id):
	post = Posts.query.get(post_id)
	if post :
		return render_template('individual_post.html',post = post)
	return abort(404,'Route Does Not Exists')


@posts.route('/post/new',methods=["GET","POST"])
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
		return redirect(url_for('main.homePage'))
	return render_template('post.html', form=form, act='New')


@posts.route('/post/delete/<int:post_id>',methods=["GET","POST"])
@login_required
def deletePostPage(post_id):
	post = Posts.query.get(post_id)
	if post :
		is_user_authenticated_post = post.user_id == current_user.id
		if is_user_authenticated_post:
			db.session.delete(post)
			db.session.commit()
			flash('Post deleted Successfully !','success')
			return redirect(url_for('users.accountPage'))
		else:
			abort(403,'UnAuthorized Access !')
	else:
		abort(404,'Route Does Not Exists')


@posts.route('/post/update/<int:post_id>',methods=["GET","POST"])
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
			return redirect(url_for('users.accountPage'))
		
		elif is_user_authenticated_post:
			form = PostForm(title=post.title, content=post.content)
			return render_template('post.html', form=form,act='Edit')
		else:
			abort(403)
			
	else:
		abort(404,'Route Does Not Exists !')


@posts.route('/comment/new/',methods=["POST"])
@login_required
def newCommentRoute():
	post_id = request.json['post_id']
	# user_id = current_user.id
	comment = request.json['comment']
	post = Posts.query.get(post_id)
	# user = User.query.get(user_id)
	if post and current_user:
		comment = Comment(author=current_user, content=comment, post=post)
		db.session.add(comment)
		db.session.commit()
		print(f'########{comment.id}-->{post.id}-->{current_user.username}')
		return jsonify(is_done=True,content=comment.content,comment_id=comment.id,username=current_user.username,post_id=post.id)
	else:
		return jsonify(is_done=False)


@posts.route('/comment/delete/',methods=["POST"])
@login_required
def deleteCommentRoute():
	post_id = request.json['post_id']
	comment_id = request.json['comment_id']

	post = Posts.query.get(post_id)
	comment = Comment.query.get(comment_id)
	if comment and post:
		if comment.author == current_user:
			db.session.delete(comment)
			db.session.commit()
			print("######deleted")
			return jsonify(is_done=True)
		else:
			return jsonify(is_done=False)
	else:
		return jsonify(is_done=False)
