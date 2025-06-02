# Movie filter app
## Setup server
You must have PostgreSQL 17.4 or newer installed (older versions might work, but we cannot guarantee it)

Install required packages from requirements.txt

Open a PostgreSQL server and save the credentials in .env file in the root folder (look at the .env-sample file for how to set database credentials).

Make sure the csv files are located in "website/data-csv/". You can get them from [this Kaggle page](https://www.kaggle.com/datasets/andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews/)

Run import_data.py (imports data from csv files to databse, takes a couple minutes). The program might seem to hang while saving reviews. This is normal intended behaviour. It will take some time for the reviews to save since there are about 1.4 million.

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
