#store standard standard root to where users can access like homepage. 
import random
from flask import Blueprint, render_template
from .models import Movie
from . import db
from  sqlalchemy.sql.expression import func, select


views = Blueprint('views', __name__)

@views.route('/')
def home():
    user = {"name": "Isak"}
    return render_template("home.html", user=user)

@views.route('/movies')
def movies():
    random_movies = Movie.query.order_by(func.random()).filter(Movie.tomato_meter > 50).filter(Movie.audience_score > 50).limit(10).all()
    return render_template("movies.html", movies=random_movies, user={"is_authenticated": False})
