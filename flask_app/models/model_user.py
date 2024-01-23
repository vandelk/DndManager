from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DB, bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data:dict ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # CREATE
    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        id = connectToMySQL(DB).query_db(query, data)
        return id

    # READ
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DB).query_db(query)

        if not results:
            return []

        instance_list = []

        for dict in results:
            #empty list     class -> instance
            instance_list.append( cls(dict) )
        return instance_list
    
    @classmethod
    def get_one_by_email(cls, data:dict):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(DB).query_db(query, data)

        if not results:
            return []
        
        dict = results[0]
        instance = cls(dict)
        return instance

    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(DB).query_db(query, data)

        if not results:
            return False

        dict = results[0]
        instance = cls(dict)
        return instance


    #UPDATE

    #DELETE
    @classmethod
    def delete_one(cls, data:dict):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(DB).query_db(query, data) #returns nothing
        

    @staticmethod
    def validator(data:dict):
        is_valid = True

        if len(data['first_name']) < 2 or not data['first_name'].isalpha():
            flash('Your first name needs to be letters and longer than 2 letters', 'err_users_first_name')
            is_valid = False

        if len(data['last_name']) < 2 or not data['last_name'].isalpha():
            flash('Your last name needs to be letters and longer than 2 letters', 'err_users_last_name')
            is_valid = False

        if len(data['email']) == 0:
            flash('Invalid Email', 'err_users_email')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email', 'err_users_email')
            is_valid = False

        if len(data['password']) < 8:
            flash('Invalid password. Needs at least 8 characters', 'err_users_password')
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash('Invalid password. Doesn\'t match.', 'err_users_confirm_password')
            is_valid = False

        if is_valid:
            #search db for email to check if unique
            potential_user = User.get_one_by_email(data)
            #if True -> already exists
            if potential_user:
                flash('Email already in use', 'err_users_email')
                is_valid = False

        return is_valid
    
    @staticmethod
    def validator_login(data:dict):
        is_valid = True

        if len(data['email']) == 0:
            # flash('Invalid credentials', 'err_users_login')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            # flash('Invalid credentials', 'err_users_login')
            is_valid = False

        if len(data['password']) < 8:
            # flash('Invalid credentials ', 'err_users_login')
            is_valid = False

        if is_valid:
            #search db for email to check if unique
            potential_user = User.get_one_by_email(data)
            #if True -> already exists
            if not potential_user:
                #for production want error message to be 'invalid credentials'
                flash('Invalid credentials', 'err_users_login')
                is_valid = False
            else:
                if not bcrypt.check_password_hash(potential_user.password, data['password']):
                    #for production want error message to be 'invalid credentials'
                    flash('Invalid credentials', 'err_users_login')
                    is_valid = False
                else:
                    session['uuid'] = potential_user.id
        else:
            flash('Invalid credentials ', 'err_users_login')

        return is_valid