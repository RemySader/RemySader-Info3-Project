import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail


app = Flask(__name__, instance_relative_config=True)
app.config["SECRET_KEY"] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user_information.db'  #creation of the database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'smartbasketlb@gmail.com'
app.config["MAIL_PASSWORD"] = os.environ['MAIL_PASSWORD'] # We set the email password value in an environment variable everytime we run the script, so it does not appear in the code
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
db = SQLAlchemy(app)

mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


app.config.from_object('config')


from app import views
from app import models