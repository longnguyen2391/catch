import os

from flask import (
    Blueprint, 
    jsonify,
    current_app, 
    url_for
)

bp = Blueprint('capture', __name__, url_prefix='/capture')

@bp.route('/preview', methods=['POST'])
def preview():
    with current_app.camera.lock: 
        picture = current_app.camera.capture_preview()

    if picture:
        return jsonify({
            'status': 'success',
            'message': url_for('static', filename="assets/preview.jpg") + "?v=" + str(os.urandom(4).hex())
        }), 200
    else: 
        return jsonify({
            'status': 'fail', 
            'message': 'no picture captured'
        }), 400
