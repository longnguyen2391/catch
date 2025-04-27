import os 
import time

import gphoto2 as gp

class Controller: 
    def __init__(self): 
        self.camera = None 
        self.context = gp.Context()
        self.timelapse_status = False

        self.setting_folders = ['imgsettings', 'capturesettings']
        self.setting = {}

        self.capture_path = os.path.join(os.path.expanduser("~"), "Pictures")

        self.connect()
        
    def connect(self):
        try:
            if self.camera:
                self.disconnect()

            self.camera = gp.Camera()
            self.camera.init(self.context)

            return True
        except gp.GPhoto2Error as e:
            print(e)
            return False
    
    def disconnect(self):  
        try: 
            self.camera.exit()
            self.camera = None
            self.status = False 

            return True
        except gp.GPhoto2Error as e:
            print(e)

            return False
             
    def is_connected(self):
        try: 
            self.camera.get_summary() 
            return True
        except gp.GPhoto2Error as e:
            print(e)
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

    def set_capture_path(self):
        pass

    def capture(self): 
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.JPG"

        file_path = os.path.join(self.capture_path, file_name)

        try: 
            capture = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            picture = self.camera.file_get(capture.folder, capture.name, gp.GP_FILE_TYPE_NORMAL)
            picture.save(file_path)

            return file_name
        except gp.GPhoto2Error as e: 
            print(file_path)
            return False