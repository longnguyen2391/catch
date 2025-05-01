import sqlite3
import click 

from flask import current_app, g 
from werkzeug.security import generate_password_hash

def get_db():
    """
        Connect to database in request if not connected via app config
        and set query return type is dictionary

        Return: 
            - g.db: database that connected
    """

    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db 

def close_db(e=None):
    """Close database connect if its connected"""

    db = g.pop('db', None)

    if db is not None: 
        db.close()

def init_db():
    """
        Connect to the database, execute schema script to create tables
        and register default account 
    """
    db = get_db() 

    with current_app.open_resource('schema.sql') as f: 
        db.executescript(f.read().decode('utf-8'))

    with db: 
        cursor = db.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]

        if user_count == 0: 
            username = 'admin'
            password = generate_password_hash('admin')

            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, password,)
            )
            
@click.command('init-db')
def init_db_command(): 
    """Initialize database from CLI"""

    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """
        Register app with database, close database when it down and able
        to using CLI command to init database.
    """
    app.teardown_appcontext(close_db) 
    app.cli.add_command(init_db_command)
