# Flask Smart Basket Application

## Setup

### Virtual Environment
Create a virtual environment on Mac or Linux:

```
mkdir myproject
cd myproject
python3 -m venv venv

. venv/bin/activate
```

Create a virtual environment on Windows:

```
mkdir myproject
cd myproject
py -3 -m venv venv

.\venv\Scripts\activate
```



## Installation

### Flask

Install Flask:

```
pip install Flask
```

### Flask Extensions

Install Flask-SQLAlchemy:

```
pip install Flask-SQLAlchemy
```

Install Flask-Mail:

```
pip install Flask-Mail
```


## Flask Application Structure


```
.
|──────app/
| |────__init__.py
| |────models.py
| |────static/
| | |────css/
| | | |────bg1.jpg
| | | |────style.css
| | |────images/
| | |────js/
| | | |────cart.js
| | | |────validate-users.js
| |────templates/
| | |────account.html
| | |────base.html
| | |────forgot.html
| | |────index.html
| | |────index2.html
| | |────reset.html
| | |────signup.html
| | |────success.html
| |────views.py
|──────config.py
|──────run.py
|──────venv/

```



## Run Flask
### Here's how you run the flask app from the terminal:

```
cd yourworkdirectory
. venv/bin/activate
python3 run.py
```

### Open in a Browser
Your running server will be visible at [http://127.0.0.1:5000](http://127.0.0.1:5000)


## Create DataBase
### Here's how you create your SQLAlchemy DataBase from the terminal:

```
python3
from app import db
db.create_all()
```

