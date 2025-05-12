import os
import json
import shutil 
import subprocess 

from flask import current_app

def count_folders_and_files():
    folder = 0 
    file = 0 

    for root, dirs, files in os.walk(current_app.camera.capture_path):
        if dirs: 
            folder += len(dirs) 
        if files: 
            file += len(files)
    
    return folder, file 

def check_disk_usage(): 
    total, used, free = shutil.disk_usage("/")
    
    return total // (2**30), used // (2**30), free // (2**30)

def save_config(data):
    with open('config.json', 'w') as f: 
        json.dump(data, f, indent=4)

def load_config(): 
    try: 
        with open('config.json', 'r') as f:
            config = json.load(f) 

            return config 
    except FileNotFoundError: 
        default = {
            'minutes': 0,
            'second': 0, 
            'enable': False
        }

        save_config(default)

        return default

def sync_files():
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'timelapsephotosync.sh')
    try: 
        result = subprocess.run(
            ["bash", script_path], 
            check=True, 
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, 
            text=True
        )

        return True, result.stdout 
    
    except subprocess.CalledProcessError as e: 
        return False, e.stdout
    