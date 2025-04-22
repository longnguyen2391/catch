from flask import (
    Blueprint,
    jsonify, 
    url_for,
    send_from_directory
)

from ..extension import camera, camera_lock

import os 

bp = Blueprint('capture', __name__, url_prefix='/capture')

@bp.route('/preview', methods=['POST'])
def preview():
    with camera_lock: 
        file = camera.capture()

    if file is not None: 
        return jsonify({
            'status': 'success',
            'message': f'{file}'
        }), 200
    else: 
        return jsonify({
            'status': 'fail', 
            'message': 'no picture captured'
        }), 400
