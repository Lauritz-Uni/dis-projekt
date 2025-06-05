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
    genre = request.args.get('genre', '')
    rating = request.args.get('rating', '')
    language = request.args.get('original_language', '')

    sanitized_query = escape(query)

    if not query:
        query = ""

    page = request.args.get('page', 1, type=int)
    limit = 15
    offset = (page - 1) * limit

    #filter for minimum and maximum runtime in minutes
    min_runtime = request.args.get("min_runtime", 0, type=int)
    max_runtime = request.args.get("max_runtime", 300, type=int)

    #filter for AVG critic scores
    min_critic = request.args.get('min_critic', 0, type=int)
    max_critic = request.args.get('max_critic', 100, type=int)
    grade = request.args.get('grade')

    # filter for top_critic scores
    min_critic = request.args.get("min_critic", 0, type=int)
    max_critic = request.args.get("max_critic", 100, type=int)

    # filter for release dates, both in theaters and for streaming services.
    min_year_theaters = request.args.get("min_year_theaters", 1900, type=int)
    max_year_theaters = request.args.get("max_year_theaters", 2025, type=int)
    min_year_streaming = request.args.get("min_year_streaming", 1990, type=int)
    max_year_streaming = request.args.get("max_year_streaming", 2025, type=int)
    
    # Get unique dropdown features
    genres = db.session.execute(text("SELECT DISTINCT genre FROM movie WHERE genre IS NOT NULL ORDER BY genre")).scalars().all()
    ratings = db.session.execute(text("SELECT DISTINCT rating FROM movie WHERE rating IS NOT NULL ORDER BY rating")).scalars().all()
    languages = db.session.execute(text("SELECT DISTINCT original_language FROM movie WHERE original_language IS NOT NULL ORDER BY original_language")).scalars().all()


    # Tomato meter filters
    min_score = request.args.get('min_score', 0, type=int)
    max_score = request.args.get('max_score', 100, type=int)

    # Main filtered query
    sql_base = """
        SELECT m.*, 
                AVG(
                    CASE
                        WHEN r.original_score ~ '^[0-9]+(\\.[0-9]+)?/[0-9]+$' THEN
                            100 * split_part(r.original_score, '/', 1)::float / NULLIF(split_part(r.original_score, '/', 2)::float, 0)
                        WHEN r.original_score ~ '^[0-9]+(\\.[0-9]+)?$' AND r.original_score::float <= 10 THEN
                            10 * r.original_score::float
                        WHEN r.original_score ~ '^[0-9]+(\\.[0-9]+)?$' THEN
                            r.original_score::float
                        ELSE NULL
                    END) AS avg_critic_score
        FROM movie m
        JOIN review r ON m.id = r.movie_id
        WHERE m.title ILIKE :search_term
            AND (m.tomato_meter IS NULL OR m.tomato_meter BETWEEN :min_score AND :max_score)
            AND (m.runtime_minutes IS NULL OR m.runtime_minutes BETWEEN :min_runtime AND :max_runtime)
            AND (EXTRACT(YEAR FROM m.release_date_theaters) BETWEEN :min_year_theaters AND :max_year_theaters)
            AND (EXTRACT(YEAR FROM m.release_date_streaming) BETWEEN :min_year_streaming AND :max_year_streaming)"""
    if grade: 
        sql_base += " AND (:grade = '' OR UPPER(TRIM(r.original_score)) = :grade)"

    sql_base +="""
        GROUP BY m.id
        HAVING AVG(
               CASE
                    WHEN r.original_score ~ '^[0-9]+(\\.[0-9]+)?/[0-9]+$' THEN
                        100 * split_part(r.original_score, '/', 1)::float / NULLIF(split_part(r.original_score, '/', 2)::float, 0)
                    WHEN r.original_score ~ '^[0-9]+(\\.[0-9]+)?$' AND r.original_score::float <= 10 THEN
                        10 * r.original_score::float
                    WHEN r.original_score ~ '^[0-9]+(\\.[0-9]+)?$' THEN
                        r.original_score::float
                    ELSE NULL
                END) BETWEEN :min_critic AND :max_critic
        ORDER BY m.title
    sql = text("""
        SELECT * FROM movie
        WHERE title ILIKE :search_term
          AND (tomato_meter IS NULL OR (tomato_meter BETWEEN :min_score AND :max_score))
          AND (:genre = '' OR genre = :genre)
          AND (:rating = '' OR rating = :rating)
          AND (:original_language = '' OR original_language = :original_language)
        ORDER BY title
        LIMIT :limit OFFSET :offset
    """
    search_sql  = text(sql_base)
    
    params = {
    'search_term': f"%{query}%",
    'min_score': min_score,
    'max_score': max_score,
    'min_runtime': min_runtime,
    'max_runtime': max_runtime,
    'min_year_theaters': min_year_theaters,
    'max_year_theaters': max_year_theaters,
    'min_year_streaming': min_year_streaming,
    'max_year_streaming': max_year_streaming,
    'min_critic': min_critic,
    'max_critic': max_critic,
        'genre': genre,
        'rating': rating,
        'original_language': language,
    'limit': limit,
    'offset': offset,
    'grade': grade.upper().strip() if grade else ''
    }

    results = db.session.execute(sql, params).fetchall()



    # Count query for pagination
    count_sql = text("""
        SELECT COUNT(*) FROM movie
        WHERE title ILIKE :search_term
          AND (tomato_meter IS NULL OR (tomato_meter BETWEEN :min_score AND :max_score))
          AND (:genre = '' OR genre = :genre)
          AND (:rating = '' OR rating = :rating)
          AND (:original_language = '' OR original_language = :original_language)
    """)
    total = db.session.execute(count_sql, {
        'search_term': f"%{query}%",
        'min_score': min_score,
        'max_score': max_score,
        'genre': genre,
        'rating': rating,
        'original_language': language
    }).scalar()


    total_pages = math.ceil(total / limit)

    user = type('user', (object,), {'is_authenticated': False})()
    return render_template(
        "search_results.html",
        movies=search_results ,
        query=sanitized_query,  
        max_score=max_score,
        min_score=min_score,
        min_runtime=min_runtime,
        max_runtime=max_runtime,
        min_year_theaters=min_year_theaters,
        max_year_theaters=max_year_theaters,
        min_year_streaming=min_year_streaming,
        max_year_streaming=max_year_streaming,
        min_critic=min_critic,
        max_critic=max_critic,
        grade=grade,
        user=user,
        page=page,
        total_pages=total_pages,
        genres=genres,
        ratings=ratings,
        languages=languages,
        genre=genre,
        rating=rating,
        original_language=language
    )
