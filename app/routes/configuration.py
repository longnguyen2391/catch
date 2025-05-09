import os

from flask import Blueprint, jsonify, request, current_app, render_template

from ..utils import count_folders_and_files, check_disk_usage, sync_files

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

@bp.route('/set', methods=['POST'])
def set():
    name = next(iter(request.form))
    value = request.form.get(name)
    
    with current_app.camera_lock: 
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

@bp.route('/status', methods=['GET'])
def status(): 
    current_status = None 

    with current_app.camera_lock:
        current_status = current_app.camera.is_connected() 

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

@bp.route('/sync', methods=['POST'])
def sync():
    result = sync_files() 

    if "error" in result.lower():
        return jsonify({
            'status': 'fail',
            'message': result
        }), 500 
    else: 
        return jsonify({
            'status': 'success',
            'message': result
        }), 200
    
@bp.route('log', methods=["GET"]) 
def log(): 
    log_file = os.path.join(current_app.root_path, 'static', 'system.log')

    with open(log_file, "r") as f: 
        content = f.read().replace("\n", "<br>")
        
        return render_template("log.html", content=content)