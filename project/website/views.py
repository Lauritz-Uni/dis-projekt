#store standard standard root to where users can access like homepage. 
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    user = {"name": "Isak"}
    return render_template("home.html", user=user)



