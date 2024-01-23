from flask import render_template, request, redirect, session
from flask_app import app, bcrypt
from flask_app.models.model_user import User
from flask_app.models.model_character import Character
from flask_app.models.model_party import Party

#DISPLAY ROUTE -> Shows the form to create a game
@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/parties')
    return render_template('login.html')

@app.route('/register')
def user_new():
    if 'uuid' in session:
        return redirect('/parties')
    return render_template('register.html')

#ACTION ROUTE -> process the form from the new route above
@app.post('/user/login')
def user_login():
    User.validator_login(request.form)
    return redirect('/parties')

@app.route('/user/logout')
def user_logout():
    del session['uuid']
    return redirect('/')

#ACTION ROUTE -> process the form from the new route above
@app.post('/user/create')
def user_create():
    #validate form
    is_valid = User.validator(request.form)

    if not is_valid:
        return redirect('/')
    
    #hash password
    hash_pw = bcrypt.generate_password_hash(request.form['password'])

    data = {
        **request.form,
        'password': hash_pw
    }

    id = User.create(data)
    session['uuid'] = id
    return redirect('/parties')

#DISPLAY ROUTE -> display user info
@app.route('/profile')
def user_show():
    if 'uuid' not in session:
        return redirect('/')
    user = User.get_one({'id': session['uuid']})
    users_chars = Character.get_users_characters({'id': session['uuid']})
    all_parties = Party.get_all()
    user_parties = Party.get_users_parties({'id': session['uuid']})
    return render_template('profile.html', characters=users_chars, all_parties=all_parties, parties=user_parties, user=user)

