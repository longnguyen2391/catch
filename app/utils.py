from time import sleep 
from shutil import disk_usage

from app.extension import camera

import os
import json

def reconnecting(): 
    while True: 
        current_status = camera.is_connected() 

        if current_status: 
            sleep(5) 
            continue 
        else: 
            camera.connect() 
            sleep(5)
            continue 

def count_folders_and_files():
    folder = 0 
    file = 0 

    for root, dirs, files in os.walk(camera.capture_path):
        if dirs: 
            folder += len(dirs) 
        if files: 
            file += len(files)
    
    return folder, file 

def check_disk_usage(): 
    total, used, free = disk_usage("/")

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