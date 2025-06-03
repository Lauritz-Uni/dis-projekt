import pandas as pd
from pandarallel import pandarallel
from datetime import datetime
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables from .env
load_dotenv('./.env')

# Environment variables
DB_NAME = 'moviesdb'
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Initialize Pandarallel
pandarallel.initialize(progress_bar=True, verbose=0)

def create_database_if_not_exists():
    """
    Creates the database if it doesn't exist.

    This function will attempt to connect to the PostgreSQL server specified by the
    environment variables DB_HOST, DB_PORT, DB_USER, and DB_PASSWORD. If the database
    specified by DB_NAME does not exist, it will be created.

    If the database already exists, this function will do nothing except print a
    message indicating that the database already exists.

    If the database cannot be created due to an error, this function will raise an
    exception with the error message.

    :return: None
    """
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f'[+] Database "{DB_NAME}" created successfully.')
        else:
            print(f'[i] Database "{DB_NAME}" already exists.')

        cur.close()
        conn.close()

    except Exception as e:
        print("[!] Error creating database:", e)
        raise

def process_movie_row(row):
    """
    Processes a row of movie data, converting and cleaning its fields.

    This function takes a row from a DataFrame containing movie data and processes its fields,
    applying type conversions, date parsing, and string handling as necessary. It uses helper
    functions to safely cast values to specified types, convert strings to datetime objects, 
    and clean genre strings.

    Args:
        row: A pandas Series representing a row of movie data.

    Returns:
        A dictionary with processed movie data where each field has been converted to the 
        appropriate type or format. Fields include 'id', 'title', 'audience_score', 'tomato_meter',
        'rating', 'rating_contents', 'release_date_theaters', 'release_date_streaming', 'runtime_minutes',
        'genre', 'original_language', 'director', 'writer', 'box_office', 'distributor', and 'sound_mix'.
    """

    import pandas as pd
    def safe_cast(value, cast_type):
        """
        Safely casts a value to the specified type if possible.

        Args:
            value: The value to be cast.
            cast_type: The type to which the value should be cast.

        Returns:
            The value cast to the specified type if casting is successful and the 
            value is not null; otherwise, None.
        """
        try:
            return cast_type(value) if pd.notnull(value) else None
        except Exception:
            return None
    def safe_date(value):
        """
        Safely converts a value to a datetime object if possible.

        Args:
            value: The value to be converted.

        Returns:
            The value converted to a datetime object if conversion is successful and the 
            value is not null; otherwise, None.
        """
        try:
            dt = pd.to_datetime(value, errors='coerce')
            return dt if pd.notnull(dt) else None
        except Exception:
            return None
    def handle_genre(input):
        """
        Processes the genre string by replacing ' & ' with ', '.

        Args:
            input: The genre string to be processed.

        Returns:
            A processed genre string with ' & ' replaced by ', ', 
            or the original genre string if an exception occurs.
        """
        genre = safe_cast(input, str)
        try:
            return genre.replace(" & ", ", ")
        except Exception:
            return genre
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
        'genre': handle_genre(row.get('genre')),
        'original_language': safe_cast(row.get('originalLanguage'), str),
        'director': safe_cast(row.get('director'), str),
        'writer': safe_cast(row.get('writer'), str),
        'box_office': safe_cast(row.get('boxOffice'), str),
        'distributor': safe_cast(row.get('distributor'), str),
        'sound_mix': safe_cast(row.get('soundMix'), str)
    }

def process_review_row(row):
    """
    Processes a row of review data, converting and cleaning its fields.

    This function takes a row from a DataFrame containing review data and processes its fields,
    applying type conversions, date parsing, and string handling as necessary. It uses a helper
    function to safely cast values to specified types and convert strings to datetime objects.

    Args:
        row: A pandas Series representing a row of review data.

    Returns:
        A dictionary with processed review data where each field has been converted to the
        appropriate type or format. Fields include 'review_id', 'movie_id', 'creation_date',
        'critic_name', 'is_top_critic', 'original_score', 'review_state', 'publication_name',
        'review_text', 'score_sentiment', and 'review_url'.
    """
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
    """
    Main entry point for the import_data script.

    This function will drop and recreate all tables in the 'moviesdb' database, then read and process
    the CSV files in website/data-csv/, and save the data to the database.

    The script will prompt the user to confirm before deleting all data in 'moviesdb'.
    """
    input("About to recreate and delete everything in 'moviesdb' database. Please close this program if you want to save the data in moviesdb.\nPress enter to continue...")
    create_database_if_not_exists()

    # Check if csv files exist
    if not os.path.exists("website/data-csv/rotten_tomatoes_movie_reviews.csv"):
        print("[!] Error: rotten_tomatoes_movie_reviews.csv file not found. Please place the file in the website/data-csv directory.")
        return

    if not os.path.exists("website/data-csv/rotten_tomatoes_movies.csv"):
        print("[!] Error: rotten_tomatoes_movies.csv file not found. Please place the file in the website/data-csv directory.")
        return

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
        print(movie_dicts[:5])
        movie_objects = [Movie(**md) for md in movie_dicts]
        print(f"[*] Saving {len(movie_objects)} movies...")
        db.session.bulk_save_objects(movie_objects)
        db.session.commit()
        print("[.] Movies imported.")

        print("[*] Reading and processing reviews...")
        reviews_df = pd.read_csv("website/data-csv/rotten_tomatoes_movie_reviews.csv")
        reviews_df.rename(columns={'id': 'movie_id'}, inplace=True) # rename id column to movie_id to match movie table
        reviews_df.drop_duplicates(subset="reviewId", inplace=True)
        review_dicts = reviews_df.parallel_apply(process_review_row, axis=1).tolist()
        valid_movie_ids = {movie.id for movie in db.session.query(Movie.id).all()}

        original_len = len(review_dicts)
        review_dicts = [r for r in review_dicts if r['movie_id'] in valid_movie_ids]
        skipped = original_len - len(review_dicts)

        print(f"[!] Skipped {skipped} reviews with unknown movie_id")
        invalid_ids = set(r['movie_id'] for r in reviews_df.to_dict('records')) - valid_movie_ids
        print(f"[!] {len(invalid_ids)} movie_ids in reviews not found in movie table. Sample: {list(invalid_ids)[:5]}")

        review_objects = [Review(**rd) for rd in review_dicts]
        print(f"[*] Saving {len(review_objects)} reviews...")
        db.session.bulk_save_objects(review_objects)
        print("[*] Comitting data...")
        db.session.commit()
        print("[.] Reviews imported and all data committed.")

if __name__ == '__main__':
    main()