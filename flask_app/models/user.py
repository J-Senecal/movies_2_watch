from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = "movies_two_watch_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.movies = []


    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, email, password)
                VALUES (%(first_name)s, %(email)s, %(password)s);"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return results
    

    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return False
        emails = []
        for row in results:
            emails.append(cls(row))
        return emails


    @staticmethod
    def validate_reg(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash("First name cannot be blank", 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format", 'reg')
            is_valid = False
        if len(user['password']) < 4:
            flash("Password must be at least 8 character long", 'reg')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords must match", 'reg')
            is_valid = False
        # check to see if email already exists
        users = User.get_all()
        emails = []
        if users:
            for row in users:
                emails.append(row.email)
            if user['email'] in emails:
                print(user['email'])
                print(emails)
                flash("Email already exists", 'reg')
                is_valid = False

        return is_valid