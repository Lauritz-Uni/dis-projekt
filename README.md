# Movie filter app
## Setup server
You must have PostgreSQL 17.4 or newer installed (older versions might work, but we cannot guarantee it)

Install required packages from requirements.txt

Open a PostgreSQL server and save the credentials in .env file in the root folder (look at the .env-sample file for how to set database credentials).

Make sure the csv files are located in "website/data-csv/". You can get them from [this Kaggle page](https://www.kaggle.com/datasets/andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews/)

Run import_data.py (imports data from csv files to databse, takes a couple minutes). The program might seem to hang while saving reviews. This is normal intended behaviour. It will take some time for the reviews to save since there are about 1.4 million.

Once finished, you can run main.py and the website will run on [http://127.0.0.1:5000](http://127.0.0.1:5000)


# Libraries and software used

## Backend
Python 3.12

[Flask](https://flask.palletsprojects.com/en/stable/) - Python web framework

[SQLAlchemy](https://www.sqlalchemy.org/) - ORM for PostgreSQL

[psycopg2](https://pypi.org/project/psycopg2/) - PostgreSQL driver

[movieposters](https://pypi.org/project/movieposters/) - For displaying getting URLs for movie posters

[markupsafe](https://pypi.org/project/MarkupSafe/) - Used to make sure users cant do XSS, hopefully

[pandas](https://pandas.pydata.org/) - For loading the csv data for our database

[pandarallel](https://pypi.org/project/pandarallel/) - Parallelizes pandas operations, making it much faster

## Database
[PostgreSQL 17.4](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) - The database software

## Frontend
Html + css + javascript - Must-use for web development

[jinja2](https://jinja.palletsprojects.com/en/stable/) - Used in our html templates to make the backend available to the frontend
