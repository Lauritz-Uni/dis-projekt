from . import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    release_date = db.Column(db.String(20))
    genre = db.Column(db.String(100))
    runtime = db.Column(db.Integer)
    pg_rating = db.Column(db.String(10))
    tomatometer = db.Column(db.Float)

    reviews = db.relationship('Review', backref='movie', lazy=True)

class Critic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    critic_name = db.Column(db.String(100))

    reviews = db.relationship('Review', backref='critic', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    sentiment = db.Column(db.String(10))
    score = db.Column(db.Float)
    itc = db.Column(db.Boolean)  # Is Top Critic

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    critic_id = db.Column(db.Integer, db.ForeignKey('critic.id'))