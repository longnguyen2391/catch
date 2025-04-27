import time
import threading

from flask import Blueprint, jsonify, request

from ..utils import save_config, load_config
from ..extension import camera, camera_lock

bp = Blueprint('timelapse', __name__, url_prefix='/timelapse')

@bp.route('/config', methods=['GET'])
def config():
    result = load_config()
        
    return jsonify({
        'status': 'success', 
        'message': result
    }), 200

@bp.route('/status', methods=['GET'])
def status(): 
    current_status = camera.get_timelapse_status() 

    return jsonify({
        'status': 'success', 
        'message': f'current timelapse status: {current_status}'
    }), 200

@bp.route('/start', methods=['POST']) 
def start(): 
    minutes = request.form.get('minutes') 
    second = request.form.get('second')
    enable = request.form.get('enable')

    save_config({'minutes': minutes, 'second': second, 'enable': enable})

    if len(minutes) == 0 or len(second) == 0: 
        return jsonify({
            'status': 'fail', 
            'message': 'invalid data' 
        }), 400
    else: 
        interval = int(minutes) * 60 + int(second) 

        camera.set_timelapse_status(True)

        def task(): 
            while camera.get_timelapse_status(): 
                
                with camera_lock: 
                    camera.capture()
                
                time.sleep(interval)

        timelapse_task = threading.Thread(target=task)
        timelapse_task.start()

        return jsonify({
            'status': 'success', 
            'message': f'timelapse start with {interval}s interval'
        }), 200
            
@bp.route('/end', methods=['GET']) 
def end(): 
    current_status = camera.get_timelapse_status()

    if current_status: 
        camera.set_timelapse_status(not current_status) 
        
        return jsonify({
            'status': 'success', 
        }), 200 
    else: 
        return jsonify({
            'status': 'fail', 
        }), 400
    