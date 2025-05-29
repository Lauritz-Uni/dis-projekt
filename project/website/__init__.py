from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from dotenv import load_dotenv
import os 

db = SQLAlchemy()
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET-KEY', 'fat mom')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
    db.init_app(app)

    from .views import views
    from. auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app 