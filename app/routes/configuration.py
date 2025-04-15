from flask import (
    Blueprint,
    request,
    jsonify
)

from ..extension import (
    camera,
    camera_lock
)

from ..utils import count_folders_and_files, check_disk_usage

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

@bp.route('/set', methods=['POST'])
def set():
    name = next(iter(request.form))
    value = request.form.get(name)
    
    with camera_lock: 
        result = camera.set_config(name=name, value=value)

        if result:
            return jsonify({
                'status': 'success', 
                'message': f'{name} is set to {value}'
            }), 200 
        else: 
            return jsonify({
                'status': 'fail', 
                'message': 'failed to set new config'
            }), 400

@bp.route('/status', methods=['GET'])
def status(): 
    current_status = None 

    with camera_lock:
        current_status = camera.is_connected() 

    return jsonify({
        'status': 'success', 
        'message': f'{current_status}'
    }), 200 

@bp.route('/storage-info', methods=['GET'])
def storage_info():
    folder, file = count_folders_and_files()
    total, used, free = check_disk_usage()

    return jsonify({
        'status': 'success',
        'message': {
            'folder': folder,
            'file': file,
            'total': total, 
            'used': used, 
            'free': free
        }
    }), 200
