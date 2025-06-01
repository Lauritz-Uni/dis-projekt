from flask import Blueprint, jsonify, render_template, request
from .models import Movie
from . import db
from  sqlalchemy.sql.expression import func, select
import movieposters as mp
from sqlalchemy import text
from markupsafe import escape

views = Blueprint('views', __name__)

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

@views.route('/search')
@views.route('/search')
def search():
    query = request.args.get('q', '')
    sanitized_query = escape(query)  # for safe HTML rendering

    if not query:
        return render_template("search_results.html", movies=[], query=sanitized_query)

    sql = text("""
        SELECT * FROM movie
        WHERE title ILIKE :search_term
    """)
    search_term = f"%{query}%"
    results = db.session.execute(sql, {'search_term': search_term}).fetchall()

    # Convert results to dicts (since raw SQL gives RowProxy objects)
    movies = []
    for row in results:
        movie = dict(row._mapping)  # for SQLAlchemy 1.4+ use row._mapping
        movies.append(movie)

    user = type('user', (object,), {'is_authenticated': False})()  # fake user
    return render_template("search_results.html", movies=movies, query=sanitized_query, user=user)
