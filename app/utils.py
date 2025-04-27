import os
import json
import shutil 
import time 

from app.extension import camera

def reconnecting(): 
    """Checking camera status and connect/reconnect with it if camera not found"""
    while True: 
        current_status = camera.is_connected() 

        if current_status: 
            time.sleep(5) 
            continue 
        else: 
            camera.connect() 
            time.sleep(5)
            continue 

def count_folders_and_files():
    """
        Counting how many folders and files is in capture path

        Return: 
            folder (int): number of folder 
            file (int): number of file
    """

    folder = 0 
    file = 0 

    for root, dirs, files in os.walk(camera.capture_path):
        if dirs: 
            folder += len(dirs) 
        if files: 
            file += len(files)
    
    return folder, file 

def check_disk_usage(): 
    """
        Checking total disk, disk used and disk free on physical server 

        Return: 
            total (int): total disk storage 
            used (int): space used in disk 
            free (int): free space in disk 
    """

    total, used, free = shutil.disk_usage("/")

    return total // (2**30), used // (2**30), free // (2**30)

def save_config(data):
    """Save data into config file"""

    with open('config.json', 'w') as f: 
        json.dump(data, f, indent=4)

def load_config(): 
    """
        Load data from config file to api. If the file does not exist then return default config.

        Return: 
            dict: 
                - 'minutes' (int): number of minutes
                - 'second' (int): number of seconds
                - 'enable' (bool): Flag to enable or disable auto start timelapse function
        
        Exception: 
            FileNotFoundError
    """
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