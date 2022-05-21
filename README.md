# Flask Smart Basket Application
## Introduction to our smart basket

Imagine yourself at the end of a long day of work. You remembered you have to go to the grocery store to buy some stuff for the house. The last thing you want to do is wait at checkout. Or even now with the corona virus going around, you may not want to put yourself at risk and wait in line with a lot of people around you, exposing yourself to the this deadly virus.

Don’t worry, we got you covered.

With our smart basket, you will never have to go through the pain of checkout again.
How you may ask?
1-You will find at your local store a self checkout station with the label ‘smart basket’ where you will be able to scan the items you want to buy.
2-Make sure to sign in to your account on our website so you can visualize the items that you are scanning.
3-At the end of your shopping you will be asked to put your card information and proceed with payment.
See, 3 easy steps that will make your shopping experience quicker, safer, and more enjoyable.
Buy smart not hard.

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
### Here's how you run the flask app from the terminal on Mac or Linux:

```
cd yourworkdirectory
. venv/bin/activate
python3 run.py
```

### Here's how you run the flask app from the terminal on windows:

```
cd yourworkdirectory
.\venv\Scripts\activate
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

