from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# ------------------------USER LOGIN/REGISTRATION---------------------------------

# INDEX PAGE for login/registration
@app.route('/')
def home():
    return render_template('index.html')

# Register new user
@app.route('/register', methods=['POST'])
def register():
    # Validate form data and display errors
    if not User.validate_reg(request.form):
        return redirect('/')
    
    # Hash password before storing
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    # Data sterilization
    data = {
        'first_name': request.form['first_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    # Save user to database and get id
    user_id = User.save(data)

    #Store session id and first name
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']

    return redirect('/dashboard')


# LOGIN
@app.route('/login', methods=['POST'])
def login():
    # Data sterilization
    data = {
        'email': request.form['email']
    }
    
    # Grab user id
    user_in_db  = User.get_one(data)

    # Check for user login validation
    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    
    #Store session id and first name
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect('/dashboard')


# LOGOUT USER
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')