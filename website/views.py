#store standard standard root to where users can access like homepage. 
from flask import Blueprint, render_template
from .models import Movie
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    user = {"name": "Isak"}
    return render_template("home.html", user=user)

@views.route('/movies')
def movies():
    movies = Movie.query.limit(10).all()
    return render_template("movies.html", movies=movies, user={"is_authenticated": False})
