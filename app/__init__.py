from flask import (
    Flask, 
    render_template
)

from app.extension import (
    camera, 
    camera_lock
)

from app.utils import reconnecting
from threading import Thread 

def create_app():
    app = Flask(__name__)

    from .routes import configuration
    app.register_blueprint(configuration.bp)

    from .routes import capture 
    app.register_blueprint(capture.bp)

    from .routes import timelapse
    app.register_blueprint(timelapse.bp)

    reconnecting_task = Thread(target=reconnecting) 
    reconnecting_task.start() 

    @app.route('/')
    def dashboard():
        with camera_lock: 
            summary = camera.get_summary()
            config = camera.get_config()
            
        return render_template('dashboard.html', config=config, summary=summary)

    return app