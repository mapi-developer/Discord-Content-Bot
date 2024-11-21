import threading
import time

clear_old_data_time = 60

def ClearOldData():
    print("data cleared")

def StartClearData():
    while True:
        time.sleep(clear_old_data_time)
        ClearOldData()

threading.Thread(target=ClearOldData).start()
print("pup")