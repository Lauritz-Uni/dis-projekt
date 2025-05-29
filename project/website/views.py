#store standard standard root to where users can access like homepage. 
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    user = {"name": "Isak"}
    return render_template("home.html", user=user)

@views.route('/movies')
def movies():
    movies = [
        {
            "title": "The Shawshank Redemption",
            "rating": 91,
            "poster": "https://m.media-amazon.com/images/..."
        },
        {
            "title": "The Godfather",
            "rating": 98,
            "poster": "https://m.media-amazon.com/images/..."
        }
    ]
    user = type('user', (object,), {'is_authenticated': False})()  # fake user
    return render_template("movies.html", movies=movies, user=user)
