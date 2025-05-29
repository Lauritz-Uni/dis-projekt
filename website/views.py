#store standard standard root to where users can access like homepage. 
from random import shuffle
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
    random_movies = Movie.query.filter(Movie.tomato_meter > 50).limit(10).all()
    return render_template("movies.html", movies=random_movies, user={"is_authenticated": False})
