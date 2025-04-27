from flask import Blueprint, render_template
from flask_login import login_required

from ..extension import camera, camera_lock

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def dashboard():
    with camera_lock: 
        summary = camera.get_summary()
        config = camera.get_config()
        
    return render_template('dashboard.html', config=config, summary=summary)