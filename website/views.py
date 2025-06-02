import math
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
def search():
    query = request.args.get('q', '')
    sanitized_query = escape(query)

    if not query:
        query = ""

    page = request.args.get('page', 1, type=int)
    limit = 15
    offset = (page - 1) * limit

    # Tomato meter filters
    min_score = request.args.get('min_score', 0, type=int)
    max_score = request.args.get('max_score', 100, type=int)

    # Main filtered query
    sql = text("""
        SELECT * FROM movie
        WHERE title ILIKE :search_term
          AND (tomato_meter IS NULL OR (tomato_meter BETWEEN :min_score AND :max_score))
        ORDER BY title
        LIMIT :limit OFFSET :offset
    """)
    results = db.session.execute(sql, {
        'search_term': f"%{query}%",
        'min_score': min_score,
        'max_score': max_score,
        'limit': limit,
        'offset': offset
    }).fetchall()
    movies = [dict(row._mapping) for row in results]

    # Count query for pagination
    count_sql = text("""
        SELECT COUNT(*) FROM movie
        WHERE title ILIKE :search_term
          AND (tomato_meter IS NULL OR (tomato_meter BETWEEN :min_score AND :max_score))
    """)
    total = db.session.execute(count_sql, {
        'search_term': f"%{query}%",
        'min_score': min_score,
        'max_score': max_score
    }).scalar()
    total_pages = math.ceil(total / limit)

    user = type('user', (object,), {'is_authenticated': False})()
    return render_template(
        "search_results.html",
        movies=movies,
        query=sanitized_query,  
        max_score=max_score,
        min_score=min_score,
        user=user,
        page=page,
        total_pages=total_pages
    )
