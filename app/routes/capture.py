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
        filename = camera.capture()

    if filename is not None: 
        filename = os.path.basename(filename)
        
        return jsonify({
            'status': 'success',
            'message': f'/images/{filename}'
        }), 200
    else: 
        return jsonify({
            'status': 'fail', 
            'message': 'no picture captured'
        }), 400
    
@bp.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(camera.capture_path, filename)
    
