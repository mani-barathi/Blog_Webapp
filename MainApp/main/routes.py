from flask import render_template,request,redirect,url_for,Blueprint
from flask_login import  current_user
from sqlalchemy import desc
from MainApp.models import Posts

main = Blueprint('main',__name__)

@main.route('/',methods=['GET','POST'])
def homePage():
	posts = []
	if current_user.is_authenticated:
		page = request.args.get('page',1,type=int)
		posts = Posts.query.order_by(desc(Posts.id)).paginate(per_page=5,page=page)
	return render_template('index.html',posts=posts)