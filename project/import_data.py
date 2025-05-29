import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from website.models import Movie, Review
from website import create_app, db

load_dotenv() # Load env variables
DATABASE_URL = os.getenv("DATABASE_URL")
