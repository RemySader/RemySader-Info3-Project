from crypt import methods
from datetime import datetime

from flask import (flash, jsonify, redirect, render_template, request, session,
                   url_for)
from itsdangerous import SignatureExpired, URLSafeTimedSerializer

from app import app, db, mail, s
from app.models import Users

from flask_mail import Message
from importlib_metadata import method_cache





@app.route('/')
def index():
    return render_template('index.html')   #this is the home page



@app.route('/account')
def account_page():
    return render_template('account.html')   #this is the login page





@app.route('/login', methods=['POST'])              #we want to verify if the user is entering his real informations and that he already created an account
def login():
    form = request.form
    user = Users.query.filter_by(email=form['email-address']).first()  #We get the user's informations from the mail he entered in the login page
    if not user:
        flash('User does not exist!!')
        return redirect(url_for('account_page'))  #if we don't find the user's information from the database, that means the user does not exist and he can not login
    if user.confirmed == False:
        flash('Please confirm your email!!')
        email = request.form['email-address']

        token = s.dumps(email, salt='email-confirm')

        msg = Message('Confirm Email', sender='smartbasketlb@gmail.com', recipients=[email])   #we store the user's email so send him the verification link

        link = url_for('confirm_email', token=token, _external=True)    #link of mail

        msg.body = f"To complete your Smart Basket account, please verify your email address by clicking the following link: {link}"  #this is the message that the user will get to verify his email

        mail.send(msg)  

        return '<h1>Please check your email address to complete your Smart Basket Account</h1>'
        # return redirect(url_for('account_page'))  #Every user get a verification link once they signup, and they can not login if they don't verify their email
    if user.check_password(form['password']):
        session['user'] = user.id
        return redirect(url_for('index2'))  # if the user exists and he entered his password correctly, we will create a session for him
    else:
        flash('Password was incorrect!!')
        return redirect(url_for('account_page')) # if the password is incorrect, the user can not login





@app.route('/signup')        
def signup_page():
    return render_template('signup.html')     #this is the signup page





@app.route('/success', methods=['POST'])   #we want to verify if the user registred succesfully
def register_user():
    form = request.form
    user = Users(
        first_name=form['first-name'],
        last_name=form['last-name'],
        email=form['email-address'],
        confirmed = False
    )                                          #we take the informations that user entered in the signup form and we store them in the database
    user.set_password(form['password'])        #the user's password will be hashed in the database
    db.session.add(user)
    db.session.commit()                        #we store the user's informations in the database
 
    email = request.form['email-address']

    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', sender='smartbasketlb@gmail.com', recipients=[email])   #we store the user's email so send him the verification link

    link = url_for('confirm_email', token=token, _external=True)    #link of mail

    msg.body = f"To complete your Smart Basket account, please verify your email address by clicking the following link: {link}"  #this is the message that the user will get to verify his email

    mail.send(msg)  

    return '<h1>Please check your email address to complete your Smart Basket Account</h1>'





@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=300)    #we make sure that the user clicked on the link before it expired 
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






@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot.html')    #this the forgot password page






@app.route('/reset_password', methods=['POST'])
def reset_password():
    form = request.form
    user = Users.query.filter_by(email=form['email-address']).first()    
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
        email = s.loads(token, salt='password-reset', max_age=3600) #we make sure that the user clicked on the link before it expired 
    except SignatureExpired:
        return '<h1>This link is invalid or has expired</h1>'    #if the link expired, he will get this error
    
    user = Users.query.filter_by(email=email).first()         #if he clicked the link on time we store his infos

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
                user.set_password(form['password'])     #we change his password in the database
                db.session.add(user)
                db.session.commit()
                session.pop('user', None)
        except:
            return '<h1>Error</h1>'            #if the user is not logged in and tries to access this page, he will get an error

        flash('Password changed succesfully.')
        return redirect(url_for('account_page'))






@app.route('/validate-users', methods=['POST'])          #we want to verify that the email entered in the signup page has not been already use
def validate_users():
    if request.method == "POST":
        email_address = request.get_json()['email']
        user = Users.query.filter_by(email=email_address).first()
        if user:
            return jsonify({"user_exists": "true"})
        else:
            return jsonify({"user_exists": "false"})






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






# @app.route('/purchase', methods=['POST', 'GET'])
# def purchase():
#     purchase_date = PurchaseDate()
#     db.session.add(purchase_date)
#     db.session.commit()
#     return redirect(url_for('index2'))
