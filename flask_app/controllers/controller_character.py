from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.model_character import Character
from flask_app.models.model_user import User
from flask_app.models.model_party import Party

@app.route('/characters')
def characters():
    if 'uuid' not in session:
        return redirect('/')
    user = User.get_one({'id': session['uuid']})
    characters = Character.get_all()
    parties= Party.get_all()
    return render_template('characters.html', characters=characters, parties=parties, user=user)

@app.route('/character/new')
def character_new():
    if 'uuid' not in session:
        return redirect('/')
    user = User.get_one({'id': session['uuid']})
    return render_template('character_create.html', user=user)

@app.post('/character/create')
def character_create():
    is_valid = Character.validator(request.form)

    if not is_valid:
        return redirect('/character/new')

    data = {
        'ai_gen': 'off',
        **request.form,
        'user_id': session['uuid']
    }

    print(data)

    Character.create(data)
    return redirect('/characters')

@app.post('/character/create/origin')
def character_create_origin():
    is_valid = Character.validator(request.form)

    if not is_valid:
        return redirect('/character/new')

    data = {
        'ai_gen': 'off',
        **request.form,
        'user_id': session['uuid']
    }

    print(data)

    Character.create(data)
    return redirect('/characters')

@app.route('/character/<int:id>')
def character_show(id):
    if 'uuid' not in session:
        return redirect('/')
    
    character = Character.get_one({'id':id})
    user = User.get_one({'id': session['uuid']})
    party = Party.only_party({'id': character.party_id})
    return render_template('character_show.html', character=character, party=party, user=user)


@app.route('/character/<int:id>/edit')
def character_edit(id):
    if 'uuid' not in session:
        return redirect('/')
    
    character = Character.get_one({'id':id})
    user = User.get_one({'id': session['uuid']})
    if character.user_id != session['uuid']:
        return redirect('/characters')
    return render_template('character_edit.html',character=character, user=user)

@app.post('/character/<int:id>/update')
def character_update(id):
    is_valid = Character.validator(request.form)
    data = {
        **request.form,
        'id': id,
        'user_id': session['uuid']
    }
    if not is_valid:
        return redirect(f'/character/{id}/edit')
    
    Character.update_one(data)
    return redirect(f'/character/{id}')

@app.route('/character/<int:id>/delete')
def character_delete(id):
    if 'uuid' not in session:
        return redirect('/')
    
    character = Character.get_one({'id': id})
    user = User.get_one({'id': session['uuid']})
    if character.user_id != session['uuid']:
        return redirect('/characters')
    
    Party.decrease_amount({'id': character.party_id})
    Character.delete_one({'id': id})
    return redirect('/characters')