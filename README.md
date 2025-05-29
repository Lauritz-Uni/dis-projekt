# Movie filter app
## Setup database
You must have PostgreSQL 17.4 or newer installed (older versions might work, but we cannot guarantee it)

Open a PostgreSQL server and create a database named moviesdb

Edit website/__init__.py such that it connects to the moviesdb database

Install required packages from requirements.txt

Make sure the csv files are located in website/data-csv/

Run import_data.py (imports data from csv files to databse, takes a couple minutes)

Once finished, you can run main.py and the website will run on [http://127.0.0.1:5000](http://127.0.0.1:5000)

# TODO

## Backend
[FastAPI](https://fastapi.tiangolo.com/)(Python web framework, skulle være ret easy at lære)

[SQLAlchemy](https://www.sqlalchemy.org/)(ORM for PostgreSQL)

[Alchemy](https://alembic.sqlalchemy.org/)(migrations? skulle være ret brugbar)

[psycopg2](https://pypi.org/project/psycopg2/)(PostgreSQL driver)

## Database
PostgreSQL

## Frontend
Enten React (mere kraftfuld) eller jinja2 + htmx (lettere at lave)
