import time
import threading

from flask import Blueprint, jsonify, request, current_app

from ..utils import save_config, load_config

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
    current_status = current_app.camera.get_timelapse_status() 

    return jsonify({
        'status': 'success', 
        'message': f'{current_status}'
    }), 200

@bp.route('/start', methods=['POST']) 
def start(): 
    minutes = request.form.get('minutes') 
    second = request.form.get('second')
    enable = request.form.get('enable')

    if len(minutes) == 0 or len(second) == 0: 
        return jsonify({
            'status': 'fail', 
            'message': 'invalid data' 
        }), 400
    else: 
        save_config({'minutes': minutes, 'second': second, 'enable': enable})
        interval = int(minutes) * 60 + int(second) 

        timelapse_task = threading.Thread(target=current_app.camera.timelapse, args=(interval,))
        timelapse_task.start()

        return jsonify({
            'status': 'success', 
            'message': f'timelapse start with {interval}s interval'
        }), 200
            
@bp.route('/end', methods=['GET']) 
def end(): 
    current_status = current_app.camera.get_timelapse_status()

    if current_status: 
        current_app.camera.set_timelapse_status(not current_status) 
        
        return jsonify({
            'status': 'success', 
            'message': 'timelapse ended'
        }), 200 
    else: 
        return jsonify({
            'status': 'fail', 
            'message': 'error occurs while stop timelapse'
        }), 400
    