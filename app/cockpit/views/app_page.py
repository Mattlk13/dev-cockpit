from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


app_page = Blueprint('app_page', __name__, template_folder='templates')
@app_page.route('/app/<name>')
def show(name):
    return "app page of " + name

