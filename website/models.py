from . import db

# TODO: Add movie poster

class Movie(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    audience_score = db.Column(db.Integer)
    tomato_meter = db.Column(db.Integer)
    rating = db.Column(db.String)
    rating_contents = db.Column(db.String)
    release_date_theaters = db.Column(db.Date)
    release_date_streaming = db.Column(db.Date)
    runtime_minutes = db.Column(db.Integer)
    genre = db.Column(db.String)
    original_language = db.Column(db.String)
    director = db.Column(db.String)
    writer = db.Column(db.String)
    box_office = db.Column(db.String)
    distributor = db.Column(db.String)
    sound_mix = db.Column(db.String)
    reviews = db.relationship('Review', backref='movie', lazy=True)

class Review(db.Model):
    review_id = db.Column(db.String, primary_key=True)
    movie_id = db.Column(db.String, db.ForeignKey('movie.id'), nullable=False)
    creation_date = db.Column(db.Date)
    critic_name = db.Column(db.String)
    is_top_critic = db.Column(db.Boolean)
    original_score = db.Column(db.String)
    review_state = db.Column(db.String)
    publication_name = db.Column(db.String)
    review_text = db.Column(db.Text)
    score_sentiment = db.Column(db.String)
    review_url = db.Column(db.String)