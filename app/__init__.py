import os 
import datetime 
import threading 

from flask import Flask, session
from flask_login import LoginManager

from app.utils import reconnecting
from app.user import User

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
        SESSION_PERMANENT = True 
    )

    app.permanent_session_lifetime = datetime.timedelta(minutes=30)

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    from . import db
    db.init_app(app)

    with app.app_context():
        if not os.path.exists(app.config['DATABASE']):
            db.init_db()

    from .routes import auth 
    app.register_blueprint(auth.bp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.get(id)

    from .routes import configuration
    app.register_blueprint(configuration.bp)

    from .routes import capture 
    app.register_blueprint(capture.bp)

    from .routes import timelapse
    app.register_blueprint(timelapse.bp)

    from .routes import dashboard 
    app.register_blueprint(dashboard.bp)

    reconnecting_task = threading.Thread(target=reconnecting) 
    reconnecting_task.start() 

    return app
