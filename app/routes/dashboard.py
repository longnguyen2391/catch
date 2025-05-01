from flask import Blueprint, render_template
from flask_login import login_required

from ..extension import camera, camera_lock

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def dashboard():
    with camera_lock: 
        config = camera.get_config() 
        summary = camera.get_summary()
    return render_template('dashboard.html')