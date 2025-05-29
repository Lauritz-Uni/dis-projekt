import pandas as pd
from website import create_app, db
from website.models import Movie, Review
from datetime import datetime

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Load Movies
    movies_df = pd.read_csv("website/data-csv/rotten_tomatoes_movies.csv")
    for _, row in movies_df.iterrows():
        movie = Movie(
            id=row['id'],
            title=row['title'],
            audience_score=row['audienceScore'],
            tomato_meter=row['tomatoMeter'],
            rating=row['rating'],
            rating_contents=row['ratingContents'],
            release_date_theaters=pd.to_datetime(row['releaseDateTheaters'], errors='coerce'),
            release_date_streaming=pd.to_datetime(row['releaseDateStreaming'], errors='coerce'),
            runtime_minutes=row['runtimeMinutes'],
            genre=row['genre'],
            original_language=row['originalLanguage'],
            director=row['director'],
            writer=row['writer'],
            box_office=row['boxOffice'],
            distributor=row['distributor'],
            sound_mix=row['soundMix']
        )
        db.session.add(movie)

    # Load Reviews
    reviews_df = pd.read_csv("website/data-csv/rotten_tomatoes_movie_reviews.csv")
    for _, row in reviews_df.iterrows():
        review = Review(
            review_id=str(row['reviewId']),
            movie_id=row['id'],
            creation_date=pd.to_datetime(row['creationDate'], errors='coerce'),
            critic_name=row['criticName'],
            is_top_critic=row['isTopCritic'],
            original_score=row['originalScore'],
            review_state=row['reviewState'],
            publication_name=row['publicatioName'],
            review_text=row['reviewText'],
            score_sentiment=row['scoreSentiment'],
            review_url=row['reviewUrl']
        )
        db.session.add(review)

    db.session.commit()
    print("CSV data loaded into database.")
