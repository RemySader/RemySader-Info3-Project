from datetime import datetime
from email.policy import default

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class Users(db.Model):                              #we create the user's table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime(timezone=True), nullable=True)
    purchase_history = db.Column(db.String(), nullable=False, default='')
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)      #this function will hash the password so we can store it in the database in a more secure way

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)   #this function verifies if the user entered his password when he wants to login

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name}, {self.email}, {self.confirmed})"


class Product(db.Model):                          #we create the products table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    userid=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)   #Relation between users and the product onetomany, one user can have many products 
    

    def __repr__(self):
        return f"Product('{self.name}',' {self.price}',for'{self.quantity}'Kg')"

