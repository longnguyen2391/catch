import time 
import os

timestamp = time.strftime("%Y%m%d_%H%M%S")
capture_path = os.path.join(os.path.expanduser("~"), "Pictures")

folder_name = time.strftime("%Y%m%d") 
file_name = f"{timestamp}.JPG"

os.makedirs(os.path.join(capture_path, folder_name), exist_ok=True)
 
file_path = os.path.join(capture_path, folder_name, file_name)

print(file_path)