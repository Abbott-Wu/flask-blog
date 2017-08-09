from flask import render_template
from flask_login import current_user
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404page.html.j2'), 404


@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500page.html.j2'), 500
