# gv_cinema_system
This is a django based movies listing application which provides the listing of movies with some filters and also the details view of each movie.

### Pre-reqs:
* Python: 3.6+
* Database: Postgres
* Create database and update its information accordingly in settings file.

### Setup Application:
* Install required pacakges:<br>
    `pip install -r requirements.txt`
    
* Move inside application directory:<br>
   `cd gv_cinema_app`

* Run migration to create db schema:<br>
    `python manage.py migrate`
    <br>
    I've also written a custom migration which will ingest the 
    movies in db using json file that you shared

* Run static collection so static files can be served:<br>
    `python manage.py collectstatic`
    
    
* Finally run application server:<br>
    `python manage.py runserver`
    
After running the server you can access it using http://127.0.0.1:8000/

### Run Application tests:
* To run django application tests:<br>
    `python manage.py test`