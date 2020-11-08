from flask import Blueprint,render_template

errors = Blueprint('errors',__name__)

# if we use errors.errorhandler(404) --> only for that particular blueprint it will be applied
# if we use errors.app_errorhandler(404) -->will be applied for the entire project

@errors.app_errorhandler(404)
def error404(error):
	return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error403(error):
	return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error500(error):
	return render_template('errors/500.html'), 500

