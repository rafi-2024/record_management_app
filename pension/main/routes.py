from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html", title= "Index")