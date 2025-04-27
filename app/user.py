from flask_login import UserMixin 
from .db import get_db

class User(UserMixin):
    def __init__(self, id, username): 
        self.id = id 
        self.username = username 

    @staticmethod
    def get(id): 
        """
            Connect to database, find user based on given id, if user found
            then return an User instance with id and username from database

            Parameters: 
                - id (int): id to find user in database
            
            Return: 
                - User: An User class instance 
                - None: if the database does not have any user with given id
        """
        db = get_db()
        cursor = db.execute('SELECT * FROM user WHERE id = ?', (id,))

        user = cursor.fetchone()
        
        if user: 
            return User(user['id'], user['username'])
        return None