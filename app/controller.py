import os 
import time

import gphoto2 as gp

class Controller: 
    def __init__(self, logger): 
        self.camera = None 
        self.context = gp.Context()
        self.logger = logger
        self.capture_path = os.path.join(os.path.expanduser("~"), "Pictures")

        self.timelapse_status = False
        self.setting = {}

        # Calling connect method to initialize with camera
        self.connect()
        self.logger.info("Camera initialize")
         
    def connect(self):
        try:
            # Clear camera
            if self.camera:
                self.logger.info("Disconnecting with camera before connect")
                self.disconnect()

            # Connect and initial context
            self.camera = gp.Camera()
            self.camera.init(self.context)
            
            self.logger.info("Camera connected successfully")
            return True
        except gp.GPhoto2Error as error:

            self.logger.warning(f"Error when connecting to camera: {error}")
            return False
    
    def disconnect(self):  
        try: 
            # Calling libgphoto2 api to exit camera and clear
            self.camera.exit()
            self.camera = None
            self.status = False 

            self.logger.info("Manually disconnected from camera")
            return True
        except gp.GPhoto2Error as error:

            self.logger.warning(f"Error when disconnecting from camera: {error}")
            return False
             
    def is_connected(self):
        try: 
            # Calling libgphoto2 api to check if camera connected?
            self.camera.get_summary() 

            self.logger.info("Camera is working")
            return True
        except gp.GPhoto2Error as error:
            
            self.logger.warning(f"Error when checking camera status: {error}")
            return False

    def get_config(self): 
        # Calling libgphoto2 api to get list of config 
        config = self.camera.get_config()

        # Choosing main config fields of camera
        for folder in ['imgsettings', 'capturesettings', 'status']:
            # Get child config object 
            child = config.get_child_by_name(folder)
            
            # Get information for each child 
            for i in range(child.count_children()): 
                sub_child = child.get_child(i)

                # Get only childs that have input value is number or range
                if sub_child.get_type() in [3, 5, 6]: 
                    self.setting[sub_child.get_name()] = {
                        'current_value': sub_child.get_value(), 
                        'choices': [sub_child.get_choice(j) for j in range(sub_child.count_choices())]
                    }
                
                # Get only childs that have text value and readonly
                if sub_child.get_type() in [2]: 
                    self.setting[sub_child.get_name()] = {
                        'current_value': sub_child.get_value(),
                        'choices': None
                    }
        
        return self.setting

    def get_timelapse_status(self): 
        return self.timelapse_status

    def set_timelapse_status(self, value): 
        # Checking value is legit or not
        if type(value) is not bool:
            raise TypeError
        else: 
            self.timelapse_status = value

    def set_config(self, name, value):
        # Type casting if given value is not string
        if type(value) is int:
            value = str(value) 
        
        try: 
            # Calling libgphoto2 api to get list of camera config 
            config = self.camera.get_config()

            # Get the name of the config that user want to modify
            target_config = config.get_child_by_name(name)

            # Checking if new value is match with target config choices? 
            if value not in [target_config.get_choice(i) for i in range(target_config.count_choices())]:
                return False

            # Calling libgphoto2 api to set new value and save current config
            target_config.set_value(value)
            self.camera.set_config(config)

            self.logger.info(f"Successfully set {name} config to {value}")
            return True
        except gp.GPhoto2Error as error: 

            self.logger.warning(f"Error when setting new value to {name}: {error}")
            return False

    def capture(self): 
        # Get captured timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Create folder and file name by timestamp 
        folder_name = time.strftime("%Y%m%d") 
        file_name = f"{timestamp}.JPG"

        # Create folder if not existed 
        os.makedirs(folder_name, exist_ok=True)

        # Create final file path 
        file_path = os.path.join(self.capture_path, folder_name, file_name)

        try: 
            # Calling libgphoto2 api to capture and save picture to file path
            capture = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            picture = self.camera.file_get(capture.folder, capture.name, gp.GP_FILE_TYPE_NORMAL)
            picture.save(file_path)

            self.logger.info(f"Picture captured: {file_path}")
            return file_name
        except gp.GPhoto2Error as error: 

            self.logger.error(f"Error when capturing: {error}")
            return False