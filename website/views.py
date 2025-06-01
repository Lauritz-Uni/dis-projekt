#store standard standard root to where users can access like homepage. 
import random
from flask import Blueprint, jsonify, render_template
from .models import Movie
from . import db
from  sqlalchemy.sql.expression import func, select
import movieposters as mp

views = Blueprint('views', __name__)

print("s" if 1+1==2 else "")

@views.route('/')
def home():
    user = {"name": "Isak"}
    return render_template("home.html", user=user)

@views.route('/movies')
def movies():
    random_movies = Movie.query.filter(Movie.tomato_meter != None, Movie.audience_score != None).order_by(Movie.tomato_meter.desc(), Movie.audience_score.desc()).limit(10).all()
    user = type('user', (object,), {'is_authenticated': False})()  # fake user
    return render_template("movies.html", movies=random_movies, user=user)

@views.route('/poster/<movie_title>')
def get_poster(movie_title):
    # Check if in database
    if Movie.query.filter_by(title=movie_title).first() is None:
        return jsonify({'poster': None})
    try:
        poster_url = mp.get_poster(movie_title)
        return jsonify({'poster': poster_url})
    except Exception as e:
        return jsonify({'poster': None})
