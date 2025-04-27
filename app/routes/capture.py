from flask import Blueprint, jsonify, send_from_directory


from ..extension import camera, camera_lock

import os 

bp = Blueprint('capture', __name__, url_prefix='/capture')

@bp.route('/preview', methods=['POST'])
def preview():
    with camera_lock: 
        filename = camera.capture()

    if filename is not None: 
        return jsonify({
            'status': 'success',
            'message': f'/capture/{filename}'
        }), 200
    else: 
        return jsonify({
            'status': 'fail', 
            'message': 'no picture captured'
        }), 400

@bp.route('/<filename>', methods=['GET'])
def get_image(filename): 
    return send_from_directory(camera.capture_path, filename)
