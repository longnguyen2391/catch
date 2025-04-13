from threading import Lock
from app.controller import Controller 

camera = Controller() 
camera_lock = Lock()