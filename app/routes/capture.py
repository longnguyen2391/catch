from flask import Blueprint, jsonify, send_from_directory, current_app

bp = Blueprint('capture', __name__, url_prefix='/capture')

@bp.route('/preview', methods=['POST'])
def preview():
    with current_app.camera_lock: 
        filename = current_app.camera.capture()

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
    # Get picture file path from physical server storage
    return send_from_directory(current_app.camera.capture_path, filename)
