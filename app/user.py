from flask_login import UserMixin 

from .db import get_db

class User(UserMixin):
    def __init__(self, id, username): 
        self.id = id 
        self.username = username 

    @staticmethod
    def get(id): 
        db = get_db()
        cursor = db.execute('SELECT * FROM user WHERE id = ?', (id,))

        user = cursor.fetchone()
        
        if user: 
            return User(user['id'], user['username'])
        return None