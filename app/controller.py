import os 
import time
import logging 

import gphoto2 as gp
from flask import current_app

class Controller: 
    def __init__(self, logger): 
        self.camera = None 
        self.context = gp.Context()
        self.timelapse_status = False

        self.setting_folders = ['imgsettings', 'capturesettings']
        self.setting = {}
        self.logger = logger 

        self.capture_path = os.path.join(os.path.expanduser("~"), "Pictures")

        self.connect()
        self.logger.info("Camera initialize")
         
    def connect(self):
        try:
            if self.camera:
                self.logger.info("Disconnecting with camera before connect")
                self.disconnect()

            self.camera = gp.Camera()
            self.camera.init(self.context)
            
            self.logger.info("Camera connected")
            return True
        except gp.GPhoto2Error as e:
            print(e)

            self.logger.warning("Camera disconnected")
            return False
    
    def disconnect(self):  
        try: 
            self.camera.exit()
            self.camera = None
            self.status = False 

            self.logger.info("Manually disconnected from camera")
            return True
        except gp.GPhoto2Error as e:

            self.logger.warning(f"Error occurs when trying disconnect with camera: {e}")
            return False
             
    def is_connected(self):
        try: 
            self.camera.get_summary() 

            self.logger.info("Camera is working")
            return True
        except gp.GPhoto2Error as e:
            
            self.logger.warning("Camera not found")
            return False

    def get_summary(self):
        summary = {
            'model': None,
            'capture_path': None
        }

        try: 
            abilities = self.camera.get_abilities()

            summary['model'] = abilities.model
            summary['capture_path'] = self.capture_path
        except gp.GPhoto2Error as e: 
            print(e)

        return summary

    def get_config(self): 
        config = self.camera.get_config()

        for folder in self.setting_folders:
            child = config.get_child_by_name(folder)
            
            for i in range(child.count_children()): 
                sub_child = child.get_child(i)

                if sub_child.get_type() in [3, 5, 6]: 
                    self.setting[sub_child.get_name()] = {
                        'key': sub_child,
                        'current_value': sub_child.get_value(), 
                        'choices': [sub_child.get_choice(j) for j in range(sub_child.count_choices())]
                    }
        
        return self.setting

    def get_timelapse_status(self): 
        return self.timelapse_status

    def set_timelapse_status(self, value): 
        if type(value) is not bool:
            raise TypeError
        else: 
            self.timelapse_status = value

    def set_config(self, name, value):
        if type(value) is int:
            value = str(value) 
        
        try: 
            config = self.camera.get_config()
            target_config = config.get_child_by_name(name)

            if value not in [target_config.get_choice(i) for i in range(target_config.count_choices())]:
                print(value)
                return False

            target_config.set_value(value)
            self.camera.set_config(config)

            return True
        except gp.GPhoto2Error as e: 
            print(e)
            return False

    def capture(self): 
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        folder_name = time.strftime("%Y%m%d") 
        file_name = f"{timestamp}.JPG"
        
        os.makedirs(folder_name, exists_ok=True)

        file_path = os.path.join(self.capture_path, folder_name, file_name)

        try: 
            capture = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            picture = self.camera.file_get(capture.folder, capture.name, gp.GP_FILE_TYPE_NORMAL)
            picture.save(file_path)

            self.logger.info(f"Picture captured: {file_path}")
            return file_name
        except gp.GPhoto2Error as e: 
            print(e)

            self.logger.error(f"Error when capturing: {e}")
            return False