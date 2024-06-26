from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Blogg:
    db_name = "blogg"
    def __init__(self, data):
        self.id = data["id"]
        self.description = data["description"]
        self.image = data["image"]
        self.location = data["location"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def get_all_Bloggs(cls):
        query = "SELECT * FROM bloggs"
        result = connectToMySQL(cls.db_name).query_db(query)
        bloggs = []
        if result:
            for blogg in result:
                bloggs.append(blogg)
        return bloggs

    @classmethod
    def create(cls, data):
        query = "INSERT INTO bloggs (description, image, location, user_id) VALUES (%(description)s, %(image)s,%(location)s,%(user_id)s)"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_blogg(cls, data):
        query = "UPDATE bloggs SET description=%(description)s, location = %(location)s  WHERE id = %(blogg_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_blogg(cls, data):
        query = "DELETE FROM bloggs WHERE id = %(blogg_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_blogg_by_id(cls, data):
        query = "SELECT * FROM bloggs LEFT JOIN users on bloggs.user_id = users.id WHERE bloggs.id = %(blogg_id)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def delete_users_blogg(cls, data):
        query = "DELETE FROM bloggs WHERE bloggs.user_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO likes (user_id, blogg_id) VALUES (%(id)s, %(blogg_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeLike(cls, data):
        query = "DELETE FROM likes WHERE blogg_id = %(blogg_id)s AND user_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_users_who_liked(cls, data):
        query = "SELECT user_id from likes where likes.blogg_id = %(blogg_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        uswersWhoLiked = []
        if results:
            for person in results:
                uswersWhoLiked.append(person["user_id"])
        return uswersWhoLiked

    @classmethod
    def delete_all_likes(cls, data):
        query = "DELETE FROM likes where blogg_id = %(blogg_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_blogg(data):
        is_valid = True
        if len(data["description"]) < 3:
            flash("Description be at least 3 characters!", "description")
            is_valid = False
        if not data["location"]:
            flash("Location is required!", "location")
            is_valid = False
        return is_valid

        # if not data["image"]:
        #     flash("File is required!", "image")
        #     is_valid = False
