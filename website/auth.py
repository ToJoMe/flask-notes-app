from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# auth file with all routes for authentication
# manage each route and the features


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # request the data of the user
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # check if the user instance exitst in db with query
        user = User.query.filter_by(email=email).first()
        if user:
            # user was found check password
            # function will hash both and check if they are equal
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                # login user
                login_user(user, remember=True)
                #redirect the user to home
                return redirect(url_for('views.home'))
                
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exists.', category='error')
        
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    # log out user
    logout_user()
    # redirect to login page if user is logged out
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get information from form
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # check if the user instance exitst in db with query
        user = User.query.filter_by(email=email).first()
    
        # checks for validation of data
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email is too short, must be longer than 3 characters.', category='error')
        elif len(name) < 2:
            flash('Name is too short, must be longer than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Passwords must have at least 7 characters.', category='error')
        else:
            # define user
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
             # add user to database
            db.session.add(new_user)
            db.session.commit()
            # login user
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
           
        
    return render_template("sign_up.html",  user = current_user)