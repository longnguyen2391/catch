import os

from flask import (
    Blueprint, 
    render_template,
    jsonify, 
    request, 
    current_app, 
)

from ..utils import (
    count_folders_and_files, 
    check_disk_usage, 
    sync_files
)

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

@bp.route('/set', methods=['POST'])
def set():
    name = next(iter(request.form))
    value = request.form.get(name)
    
    with current_app.camera.lock: 
        result = current_app.camera.set_config(name=name, value=value)

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

@bp.route('/get', methods=['GET'])
def get():
    with current_app.camera.lock:
        config = current_app.camera.get_config()
    
    if config: 
        return jsonify({
            'status': 'success', 
            'message': config
        }), 200 
    else: 
        return jsonify({
            'status': 'fail', 
            'message': 'failed to get camera config'
        }), 400

@bp.route('/status', methods=['GET'])
def status(): 
    with current_app.camera.lock:
        current_status = current_app.camera.is_connected() 

    return jsonify({
        'status': 'success', 
        'message': f'{current_status}'
    }), 200 

@bp.route('/storage', methods=['GET'])
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
    
@bp.route('/log', methods=["GET"]) 
def log(): 
    log_file = os.path.join(current_app.root_path, 'static/assets', 'system.log')

    with open(log_file, "r") as f: 
        content = f.read().replace("\n", "<br>")
        
        return render_template("log.html", content=content)