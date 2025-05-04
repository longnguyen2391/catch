from flask import Blueprint, render_template, current_app
from flask_login import login_required
from gphoto2 import GPhoto2Error

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def dashboard():
    try: 
        with current_app.camera_lock: 
            config = current_app.camera.get_config() 
            summary = current_app.camera.get_summary()
    except GPhoto2Error as error: 
        return render_template('error.html', error=error)
    
    return render_template('dashboard.html', config=config, summary=summary)