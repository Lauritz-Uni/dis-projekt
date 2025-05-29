#store standard standard root to where users can access like homepage. 
import random
from flask import Blueprint, jsonify, render_template
from .models import Movie
from . import db
from  sqlalchemy.sql.expression import func, select
import movieposters as mp


views = Blueprint('views', __name__)

@views.route('/')
def home():
    user = {"name": "Isak"}
    return render_template("home.html", user=user)

@views.route('/movies')
def movies():
    random_movies = Movie.query.order_by(func.random()).filter(Movie.tomato_meter > 50).filter(Movie.audience_score > 50).limit(10).all()
    return render_template("movies.html", movies=random_movies, user={"is_authenticated": False})

@views.route('/poster/<movie_title>')
def get_poster(movie_title):
    try:
        poster_url = mp.get_poster(movie_title)
        return jsonify({'poster': poster_url})
    except Exception as e:
        return jsonify({'poster': None})