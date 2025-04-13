from time import sleep 
from app.extension import camera

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