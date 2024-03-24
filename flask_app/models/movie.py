from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Movie:
    db = "movies_two_watch_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.friend = data['friend']
        self.date = data['date']
        self.watched = data['watched']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.movie_user = None


    @classmethod
    def save_movie(cls, data):
        query = """INSERT INTO movies (title, friend, date, watched, users_id)
                VALUES (%(title)s, %(friend)s, %(date)s, %(watched)s, %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_one_movie_by_id(cls, data):
        query = """SELECT * FROM movies WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_users_movies(cls, data):
        # print(data)
        query = """SELECT * FROM movies WHERE users_id = %(users_id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        movies = []
        # print(results)
        if results:
            for row in results:
                a_movie = cls(row)
                movies.append(a_movie)
        return movies

    @classmethod
    def delete_movie(cls, data):
        query = """DELETE FROM movies WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def update_movie(cls, data):
        query = """UPDATE movies SET title = %(title)s, friend = %(friend)s,
                date = %(date)s, watched = %(watched)s 
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def get_by_title(cls, title_data):
        data = {
            'title': title_data
        }
        query = """SELECT * FROM movies WHERE title = %(title)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return cls(results[0])
    
    
    @staticmethod
    def validate_movie(data):
        is_valid = True
        if len(data['title']) < 2:
            flash("Title must be at least 2 characters")
            is_valid = False
        if len(data['friend']) < 2:
            flash("Friend must be at least 2 characters")
            is_valid = False
        # if Movie.get_by_title(data['title']) != False:
        #     flash("Title already exists")
        #     is_valid = False
        if not data['date']:
            flash("Date required")
            is_valid = False

        return is_valid