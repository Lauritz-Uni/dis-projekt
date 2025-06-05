# Movie filter app
## Compiling and running app:
### Setup server
You must have PostgreSQL 17.4 or newer installed (older versions might work, but we cannot guarantee it)

Install required packages from requirements.txt

Open a PostgreSQL server and save the credentials in .env file in the root folder (look at the .env-sample file for how to set database credentials).

Make sure the csv files are located in "website/data-csv/". You can get them from [this Kaggle page](https://www.kaggle.com/datasets/andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews/)

Run import_data.py (imports data from csv files to databse, takes a couple minutes). The program might seem to hang while saving reviews. This is normal intended behaviour. It will take some time for the reviews to save since there are about 1.4 million.

Once finished, you can run main.py and the website will run on [http://127.0.0.1:5000](http://127.0.0.1:5000)


## Interacting with app:
You start at the Home page. Via. the navigation bar you have the option to either view a curation of Top Movies by pressing "Movies", Log in og Sign up by pressing "Login" or "Sign Up", or search for specific movies via. the search bar in the top right corner. 
To access the film filters you can simply press the "search" button, no typed input is needed. 

At this point you are presented with a variety of feature filters which you can alter based on your preferences, by either typing, selecting from a drop-down menu, or adjusting min-max slider bars. Once you are finished, press the "Apply Filters" button, and a list of movies matching your preferences will be generated (Please allow the movie posters some time to load :) ).

Movies are presented with title, poster, and various types of relevant information, such as genre and score received from critics, audience, and Rotten Tomatoes.
If you are interested in finding out more information about a given movie, or want to read its critic reviews, you just have to click on the movie to access them :).


## E/R Diagram
![Project_ER_Diagram](https://github.com/user-attachments/assets/7c0300bd-5dff-4725-aafb-51591dbb512d)


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

[Bootstrap](https://getbootstrap.com) - To make the website look clean

## Database
[PostgreSQL 17.4](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) - The database software

## Frontend
Html + css + javascript - Must-use for web development

[jinja2](https://jinja.palletsprojects.com/en/stable/) - Used in our html templates to make the backend available to the frontend
