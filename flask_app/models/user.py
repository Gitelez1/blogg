from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db_name = "blogg"
    
    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if result:
            for user in result:
                users.append(user)
            return users

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (username, email, password) VALUES(%(username)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET username = %(username)s, email = %(email)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @staticmethod
    def validate_user(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(data['username']) < 3:
            flash("Username should be at least 3 characters!", 'usernameRegister')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password should be at least 8 characters!", 'passwordRegister')
            is_valid = False
        if data['password'] != data['confirmpassword']:
            flash("Password should match!", 'confirmPasswordRegister')
        return is_valid