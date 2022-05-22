from crypt import methods
from datetime import datetime

from flask import (flash, redirect, render_template, request, session,
                   url_for)
from flask_mail import Message
from itsdangerous import SignatureExpired, URLSafeTimedSerializer

from app import app, db, mail, s
from app.models import Users

from app.password_validation import validate_pass


@app.route('/')
def index():
    return render_template('index.html')   #this is the home page



@app.route('/signup')        
def signup_page():
    return render_template('signup.html')     #this is the signup page





@app.route('/success', methods=['POST'])   #we want to verify if the user registred succesfully
def register_user():
    if request.method == "POST":
        form = request.form
        user = Users(
            first_name=form['first-name'].capitalize(),
            last_name=form['last-name'].capitalize(),
            email=form['email-address'].lower(),
            confirmed = False
        )                                          #we take the informations that user entered in the signup form and we store them in the database


        if len(user.first_name) < 2 or len(user.last_name) < 2:
            flash('First name and last name must contain at least two letters')
            return redirect(url_for('signup_page'))    #we make sure that the first and last names are at least 2 characters
        
        for char in user.first_name:
            if char.isalpha() == False:
                flash('First name must contain only letters')
                return redirect(url_for('signup_page'))     #we make sure that the first name contains only letters

        for char in user.last_name:
            if char.isalpha() == False:
                flash('Last name must contain only letters')    #we make sure that the last name contains only letters
                return redirect(url_for('signup_page'))


        if validate_pass(form['password']) == False:  #we make sure that the password entered is at least 8 characters and have at least two of: uppercase letters, lowercase letters, numbers and special characters
            flash('Password must be at least 8 characters and contain at least two of the following: uppercase letters, lowercase letters, numbers and special characters.')
            return redirect(url_for('signup_page'))

        

        user.set_password(form['password'])       #the user's password will be hashed in the database
        user_exists = Users.query.filter_by(email=user.email.lower()).first()
        if user_exists:
            flash('User already exists. Please Login instead or use a different email for Signup.')
            return redirect(url_for('signup_page'))  #if the email is already linked to another account, the user must enter another email to signup

        db.session.add(user)
        db.session.commit()                        #we store the user's informations in the database
    
        email = request.form['email-address']

        token = s.dumps(email, salt='email-confirm')

        msg = Message('Confirm Email', sender='smartbasketlb@gmail.com', recipients=[email])   #we store the user's email so send him the verification link

        link = url_for('confirm_email', token=token, _external=True)    #link of mail

        msg.body = f"To complete your Smart Basket account, please verify your email address by clicking the following link: {link}"  #this is the message that the user will get to verify his email

        mail.send(msg)  

        return '<h1>Please check your email address to complete your Smart Basket Account.</h1><br><h2>Enter your email and password in the login page to get a new verification link.</h2>'





@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=120)    #we make sure that the user clicked on the link before it expired 
    except SignatureExpired:
        return '<h1>The confirmation link is invalid or has expired</h1>' #if the link expired, he will get this error
    user = Users.query.filter_by(email=email).first()        #if he clicked the link on time we store his infos
    if user.confirmed:
        flash('Account already confirmed. Please Login.')
    else:
        user.confirmed = True                               #we turn the column 'confirmed' to True in the database and we save the time when he verified his account
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Registred Successfully. Please Login.')

    return render_template('success.html')




@app.route('/account')
def account_page():
    return render_template('account.html')   #this is the login page





@app.route('/login', methods=['POST'])              #we want to verify if the user is entering his real informations and that he already created an account
def login():
    form = request.form
    user = Users.query.filter_by(email=form['email-address'].lower()).first()  #We get the user's informations from the mail he entered in the login page
    if not user:
        flash('Incorrect email or password')
        return redirect(url_for('account_page'))  #if we don't find the user's information from the database, that means the user does not exist and he can not login
    if user.confirmed == False and user.check_password(form['password']):
        email = request.form['email-address']

        token = s.dumps(email, salt='email-confirm')

        msg = Message('Confirm Email', sender='smartbasketlb@gmail.com', recipients=[email])   #we store the user's email so send him the verification link

        link = url_for('confirm_email', token=token, _external=True)    #link of mail

        msg.body = f"To complete your Smart Basket account, please verify your email address by clicking the following link: {link}"  #this is the message that the user will get to verify his email

        mail.send(msg)  

        return '<h1>You can not Login without verifying your account. Please check your email address to complete your Smart Basket Account.</h1>'
         #Every user get a verification link once they signup, and they can not login if they don't verify their email
    if user.check_password(form['password']):
        session['user'] = user.id
        return redirect(url_for('index2'))  # if the user exists and he entered his password correctly, we will create a session for this user
    else:
        flash('Incorrect email or password')
        return redirect(url_for('account_page')) # if the password is incorrect, the user can not login






@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot.html')    #this the forgot password page







@app.route('/reset_password', methods=['POST'])
def reset_password():
    form = request.form
    user = Users.query.filter_by(email=form['email-address'].lower()).first()    
    if not user:                                                         #we store the user's infos and make sure that the user exists
        flash('User does not exist!!')
        return redirect(url_for('forgot_password'))

    session['user_id'] = user.id
    
    email = request.form['email-address']

    token = s.dumps(email, salt='password-reset')

    msg = Message('Reset Password', sender='smartbasketlb@gmail.com', recipients=[email])   

    link = url_for('password_link', token=token, _external=True)     #link of mail

    msg.body = f"Reset your password by clicking the following link: {link}"     #we send the users a link to his email so he can reset his password

    mail.send(msg)

    return '<h1>Please check your email address to reset your password</h1>'



@app.route('/password_link/<token>')
def password_link(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=120) #we make sure that the user clicked on the link before it expired 
    except SignatureExpired:
        return '<h1>This link is invalid or has expired</h1>'    #if the link expired, he will get this error
    
    user = Users.query.filter_by(email=email.lower()).first()        #if he clicked the link on time we store his infos

    session['user_id'] = user.id

    return render_template('reset.html')



@app.route('/new_password', methods=['POST', 'GET'])
def new_password():
    if request.method == "POST":
        user_id = session['user_id']
        try:
            if user_id:
                form = request.form
                user = Users.query.filter_by(id=user_id).first()   #we get the user's infos


                if validate_pass(form['password']) == False:
                    flash('Password must be at least 8 characters and contain at least two of the following: uppercase letters, lowercase letters, numbers and special characters.')
                    return render_template('reset.html')    #we make sure that the password entered is at least 8 characters and have at least two of: uppercase letters, lowercase letters, numbers and special characters


                user.set_password(form['password'])     #we change his password in the database
                db.session.add(user)
                db.session.commit()
                session.pop('user', None)
        except:
            return '<h1>Error</h1>'            #if the user is not logged in and tries to access this page, he will get an error

        flash('Password changed succesfully.')
        return redirect(url_for('account_page'))






@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user', None)                     #when the user logs out, we close the session
    return redirect(url_for('account_page'))





@app.route('/index2', methods=['POST', 'GET'])    #this is home page when the user is loggedin
def index2():
    user_id = None
    try:
        if session['user']:
            user_id = session['user']
    except:
        return '<h1>Error</h1>'            #if the user is not logged in and tries to access this page, he will get an error
    return render_template('index2.html')
