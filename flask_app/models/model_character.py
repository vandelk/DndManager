from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DB
from flask_app.models import model_user

class Character:
    def __init__(self, data:dict):
        self.id = data['id']
        self.name = data['name']
        self.race = data['race']
        self.dnd_class = data['dnd_class']
        self.background = data['background']
        self.alignment = data['alignment']
        self.backstory = data['backstory']
        self.user_id = data['user_id']
        self.party_id = data['party_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #CREATE
    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO characters (name, race, dnd_class, background, alignment, backstory, user_id) VALUES (%(name)s, %(race)s, %(dnd_class)s, %(background)s, %(alignment)s,%(backstory)s, %(user_id)s);"
        id = connectToMySQL(DB).query_db(query, data)
        return id
    
    # READ
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM characters JOIN users on characters.user_id = users.id ORDER BY characters.created_at DESC;"
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
            
        return instance_list

    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM characters JOIN users on characters.user_id = users.id WHERE characters.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)

        if not results:
            return False

        dict = results[0]
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

        return post_instance
    
    @classmethod
    def get_users_characters(cls, data:dict):
        query = "SELECT * FROM characters JOIN users on characters.user_id = users.id WHERE users.id = %(id)s;"
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

            user_instance = model_user.User(user_data)

            post_instance.user = user_instance
            instance_list.append(post_instance)
            
        return instance_list


    #UPDATE
    @classmethod
    def update_one(cls, data:dict):
        query = "UPDATE characters SET name=%(name)s, race=%(race)s, dnd_class=%(dnd_class)s, background=%(background)s, alignment=%(alignment)s, backstory=%(backstory)s WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def update_party(cls, data:dict):
        query = "UPDATE characters SET party_id=%(party_id)s WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def remove_from_party(cls, data:dict):
        query = "UPDATE characters SET party_id=null WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def remove_all_from_party(cls, data:dict):
        query = "UPDATE characters SET party_id=null WHERE party_id=%(party_id)s;"
        return connectToMySQL(DB).query_db(query, data)

    #DELETE
    @classmethod
    def delete_one(cls, data:dict):
        query = "DELETE FROM characters WHERE id = %(id)s"
        return connectToMySQL(DB).query_db(query, data) #returns nothing
    
    @staticmethod
    def validator(data:dict):
        is_valid = True

        if len(data['name']) < 1:
            flash('A name is required', 'err_character_name')
            is_valid = False

        return is_valid
        