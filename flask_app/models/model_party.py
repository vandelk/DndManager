from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DB
from flask_app.models import model_user, model_character

class Party:
    def __init__(self, data:dict):
        self.id = data['id']
        self.name = data['name']
        self.amount_characters = data['amount_characters']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #CREATE
    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO parties (name, amount_characters, user_id) VALUES (%(name)s, %(amount_characters)s, %(user_id)s);"
        id = connectToMySQL(DB).query_db(query, data)
        return id
    
    # READ
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM parties JOIN users on parties.user_id = users.id ORDER BY parties.created_at DESC;"
        results = connectToMySQL(DB).query_db(query)

        if not results:
            return []

        instance_list = []

        for dict in results:
            #empty list     class -> instance
            post_instance = cls(dict)

            user_data = {
                'id': dict['users.id'],
                'created_at': dict['users.created_at'],
                'updated_at': dict['users.updated_at'],

                'first_name': dict['first_name'],
                'last_name': dict['last_name'],
                'email': dict['email'],
                'password': dict['password']
            }

            user_instance = model_user.User(user_data)

            post_instance.user = user_instance
            instance_list.append(post_instance)

            print(len(instance_list))
            
        return instance_list

    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM parties JOIN characters on characters.party_id = parties.id JOIN users on characters.user_id = users.id WHERE parties.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)

        if not results:
            return []

        instance_list = []

        for dict in results:
            #empty list     class -> instance
            post_instance = cls(dict)

            user_data = {
                'id': dict['users.id'],
                'created_at': dict['users.created_at'],
                'updated_at': dict['users.updated_at'],

                'first_name': dict['first_name'],
                'last_name': dict['last_name'],
                'email': dict['email'],
                'password': dict['password']
            }

            character_data = {
                'id': dict['characters.id'],
                'name': dict['characters.name'],
                'created_at': dict['characters.created_at'],
                'updated_at': dict['characters.updated_at'],
                'user_id': dict['characters.user_id'],

                'race': dict['race'],
                'dnd_class': dict['dnd_class'],
                'background': dict['background'],
                'alignment': dict['alignment'],
                'backstory': dict['backstory'],
                'party_id': dict['party_id']
            }

            user_instance = model_user.User(user_data)
            character_instance = model_character.Character(character_data)

            post_instance.user = user_instance
            post_instance.character = character_instance
            instance_list.append(post_instance)
            
        return instance_list
    
    @classmethod
    def only_party(cls, data:dict):
        query = "SELECT * FROM parties WHERE id = %(id)s"
        results = connectToMySQL(DB).query_db(query, data)

        if not results:
            return False

        dict = results[0]
        instance = cls(dict)
        return instance
    
    @classmethod
    def get_users_parties(cls, data:dict):
        query = "SELECT * FROM parties WHERE user_id = %(id)s"
        results = connectToMySQL(DB).query_db(query, data)

        if not results:
            return []

        instance_list = []

        for dict in results:
            #empty list     class -> instance
            post_instance = cls(dict)
            instance_list.append(post_instance)
            
        return instance_list
    
    #UPDATE
    @classmethod
    def update_one(cls, data:dict):
        query = "UPDATE parties SET name=%(name)s, amount_characters=amount_characters+1 WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def increase_amount(cls, data:dict):
        query = "UPDATE parties SET amount_characters=amount_characters+1 WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def decrease_amount(cls, data:dict):
        query = "UPDATE parties SET amount_characters=amount_characters-1 WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    

    #DELETE
    @classmethod
    def delete_one(cls, data:dict):
        query = "DELETE FROM parties WHERE id = %(id)s"
        return connectToMySQL(DB).query_db(query, data) #returns nothing
    
    @staticmethod
    def validator(data:dict):
        is_valid = True

        if len(data['name']) < 1:
            flash('A name is required', 'err_character_name')
            is_valid = False

        return is_valid
