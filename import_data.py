# Imports
import pandas as pd
from pandarallel import pandarallel
from datetime import datetime

# Initialize Pandarallel
pandarallel.initialize(progress_bar=True, verbose=0)

def process_movie_row(row):
    import pandas as pd
    def safe_cast(value, cast_type):
        try:
            return cast_type(value) if pd.notnull(value) else None
        except Exception:
            return None
    def safe_date(value):
        try:
            dt = pd.to_datetime(value, errors='coerce')
            return dt if pd.notnull(dt) else None
        except Exception:
            return None
    return {
        'id': str(row['id']),
        'title': safe_cast(row['title'], str),
        'audience_score': safe_cast(row.get('audienceScore'), float),
        'tomato_meter': safe_cast(row.get('tomatoMeter'), float),
        'rating': safe_cast(row.get('rating'), str),
        'rating_contents': safe_cast(row.get('ratingContents'), str),
        'release_date_theaters': safe_date(row.get('releaseDateTheaters')),
        'release_date_streaming': safe_date(row.get('releaseDateStreaming')),
        'runtime_minutes': safe_cast(row.get('runtimeMinutes'), float),
        'genre': safe_cast(row.get('genre'), str),
        'original_language': safe_cast(row.get('originalLanguage'), str),
        'director': safe_cast(row.get('director'), str),
        'writer': safe_cast(row.get('writer'), str),
        'box_office': safe_cast(row.get('boxOffice'), str),
        'distributor': safe_cast(row.get('distributor'), str),
        'sound_mix': safe_cast(row.get('soundMix'), str)
    }

def process_review_row(row):
    import pandas as pd
    def safe_cast(value, cast_type):
        try:
            return cast_type(value) if pd.notnull(value) else None
        except Exception:
            return None
    return {
        'review_id': str(row['reviewId']),
        'movie_id': str(row['movie_id']),
        'creation_date': pd.to_datetime(row.get('creationDate'), errors='coerce'),
        'critic_name': safe_cast(row.get('criticName'), str),
        'is_top_critic': bool(row.get('isTopCritic')) if pd.notnull(row.get('isTopCritic')) else False,
        'original_score': safe_cast(row.get('originalScore'), str),
        'review_state': safe_cast(row.get('reviewState'), str),
        'publication_name': safe_cast(row.get('publicatioName'), str),
        'review_text': safe_cast(row.get('reviewText'), str),
        'score_sentiment': safe_cast(row.get('scoreSentiment'), str),
        'review_url': safe_cast(row.get('reviewUrl'), str)
    }

def main():
    from website import create_app, db
    from website.models import Movie, Review

    app = create_app()
    with app.app_context():
        print("[!] Dropping and recreating all tables...")
        db.drop_all()
        db.create_all()

        print("[*] Reading and processing movies...")
        movies_df = pd.read_csv("website/data-csv/rotten_tomatoes_movies.csv")
        movies_df.drop_duplicates(subset="id", inplace=True)
        movie_dicts = movies_df.parallel_apply(process_movie_row, axis=1).tolist()
        movie_objects = [Movie(**md) for md in movie_dicts]
        print(f"[*] Saving {len(movie_objects)} movies...")
        db.session.bulk_save_objects(movie_objects)
        db.session.commit()
        print("[.] Movies imported.")

        print("[*] Reading and processing reviews...")
        reviews_df = pd.read_csv("website/data-csv/rotten_tomatoes_movie_reviews.csv")
        reviews_df.rename(columns={'id': 'movie_id'}, inplace=True)
        reviews_df.drop_duplicates(subset="reviewId", inplace=True)
        review_dicts = reviews_df.parallel_apply(process_review_row, axis=1).tolist()
        # Get a set of valid movie IDs already in the database
        valid_movie_ids = {movie.id for movie in db.session.query(Movie.id).all()}

        original_len = len(review_dicts)

        # Filter out reviews for non-existent movies
        review_dicts = [r for r in review_dicts if r['movie_id'] in valid_movie_ids]

        skipped = original_len - len(review_dicts)
        print(f"[!] Skipped {skipped} reviews with unknown movie_id")

        invalid_ids = set(r['movie_id'] for r in reviews_df.to_dict('records')) - valid_movie_ids
        print(f"[!] {len(invalid_ids)} movie_ids in reviews not found in movie table. Sample: {list(invalid_ids)[:5]}")
        
        review_objects = [Review(**rd) for rd in review_dicts]
        print(f"[*] Saving {len(review_objects)} reviews...")
        db.session.bulk_save_objects(review_objects)
        db.session.commit()
        print("[.] Reviews imported and all data committed.")

if __name__ == '__main__':
    main()