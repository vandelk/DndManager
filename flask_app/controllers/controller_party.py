from flask import render_template, request, redirect, session
from flask_app import app, bcrypt
from flask_app.models.model_user import User
from flask_app.models.model_character import Character
from flask_app.models.model_party import Party

@app.route('/parties')
def parties_home():
    if 'uuid' not in session:
        return redirect('/')
    user = User.get_one({'id': session['uuid']})
    party = Party.get_all()
    return render_template('parties.html', parties=party, user=user)

@app.route('/parties/new')
def party_new():
    if 'uuid' not in session:
        return redirect('/')
    user = User.get_one({'id': session['uuid']})
    return render_template('party_create.html', user=user)

@app.post('/parties/create')
def party_create():
    is_valid = Party.validator(request.form)

    if not is_valid:
        return redirect('/party/new')

    data = {
        **request.form,
        'amount_characters': 0,
        'user_id': session['uuid']
    }

    Party.create(data)
    return redirect('/parties')

@app.route('/parties/<int:id>')
def party_show(id):
    if 'uuid' not in session:
        return redirect('/')
    
    party = Party.get_one({'id':id})
    if len(party) < 1:
        return redirect('/parties')
    user = User.get_one({'id': session['uuid']})
    return render_template('party_show.html', party=party, user=user)

@app.route('/parties/<int:id>/addcharacter')
def party_select_add(id):
    if 'uuid' not in session:
        return redirect('/')
    

    party = Party.only_party({'id':id}) 
    user = User.get_one({'id': session['uuid']})
    users_chars = Character.get_users_characters({'id': session['uuid']})
    count = 0
    
    for char in users_chars:
        print(char.party_id)
        if not char.party_id:
            count += 1
        
    if count == 0:
        users_chars = []
    return render_template('party_add.html', party=party, users_chars=users_chars, user=user)

@app.route('/parties/<int:party_id>/add/<int:char_id>')
def party_add(party_id, char_id):
    if 'uuid' not in session:
        return redirect('/')
    

    party = Party.only_party({'id':party_id}) 
    user = User.get_one({'id': session['uuid']})
    character = Character.get_one({'id':char_id})

    Party.increase_amount({'id': party_id})

    data = {
        'id': char_id,
        'party_id': party_id
    }

    Character.update_party(data)

    return redirect(f'/parties/{party_id}')

@app.route('/parties/<int:id>/edit')
def party_edit(id):
    if 'uuid' not in session:
        return redirect('/')
    
    party = Party.only_party({'id':id})
    user = User.get_one({'id': session['uuid']})
    if party.user_id != session['uuid']:
        return redirect('/parties')
    return render_template('party_edit.html',party=party, user=user)

@app.post('/parties/<int:id>/update')
def party_update(id):
    is_valid = Party.validator(request.form)
    data = {
        **request.form,
        'id': id,
        'user_id': session['uuid']
    }
    if not is_valid:
        return redirect(f'/parties/{id}/edit')
    
    Party.update_one(data)
    return redirect(f'/parties/{id}')

@app.route('/parties/<int:party_id>/remove/<int:char_id>')
def party_member_remove(party_id,char_id):

    Party.decrease_amount({'id': party_id})
    Character.remove_from_party({'id': char_id})

    return redirect(f'/parties/{party_id}')

@app.route('/parties/<int:id>/delete')
def party_delete(id):
    Character.remove_all_from_party({'party_id':id})
    Party.delete_one({'id': id})
    return redirect('/parties')