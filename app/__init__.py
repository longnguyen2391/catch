import os 
import datetime 
import time
import threading 
import logging

from flask import Flask, session
from flask_login import LoginManager

from app.user import User 
from app.controller import Controller

def create_app():
    app = Flask(__name__)

    # Load app configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
        SESSION_PERMANENT = True 
    )

    app.permanent_session_lifetime = datetime.timedelta(minutes=30)

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # Initialize sqlite3 database
    from . import db
    db.init_app(app)

    with app.app_context():
        if not os.path.exists(app.config['DATABASE']):
            db.init_db()
    
    # Configuring authentication function with flask-login 
    from .routes import auth 
    app.register_blueprint(auth.bp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.get(id) 
    
    # Configurating logger for camera controller
    logger = logging.getLogger("system") 
    logger.setLevel(logging.INFO) 

    log_file = os.path.join(app.root_path, 'static', 'system.log') 
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Register share resources
    camera = Controller(logger=logger) 
    app.camera = camera 

    camera_lock = threading.Lock() 
    app.camera_lock = camera_lock 

    # Register blueprints 
    from .routes import configuration
    app.register_blueprint(configuration.bp)

    from .routes import capture 
    app.register_blueprint(capture.bp)

    from .routes import timelapse
    app.register_blueprint(timelapse.bp)

    from .routes import dashboard 
    app.register_blueprint(dashboard.bp)

    # Thread running in background to connect camera whenever its disconnected
    def reconnecting(): 
        SAFETY_CHECK_TIME = 3000 
        RECONNECT_TIME = 60

        with app.app_context(): 
            while True: 
                if app.camera.is_connected(): 
                    time.sleep(SAFETY_CHECK_TIME) 
                    continue 
                else: 
                    app.camera.connect() 
                    time.sleep(RECONNECT_TIME)
                    continue 

    reconnecting_task = threading.Thread(target=reconnecting) 
    reconnecting_task.start() 

    # Ready to go
    return app
