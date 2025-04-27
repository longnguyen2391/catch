import threading

from app.controller import Controller 

#camera instance to do operations via Controller class methods
camera = Controller() 

#camera resource lock ensure that no both thread using one camera
camera_lock = threading.Lock() 