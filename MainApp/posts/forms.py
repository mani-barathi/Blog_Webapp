from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired(),Length(min=4,max=100)])
	content = TextAreaField('Content',validators=[DataRequired()])