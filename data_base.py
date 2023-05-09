import ctypes
import time

def print_count():
    ctypes.windll.user32.LockWorkStation()
    while 1:
        if ctypes.windll.user32.GetForegroundWindow() != 0:  # while not on lockscreen.
            time.sleep(1)
            print(ctypes.windll.user32.GetForegroundWindow())
            # predict -> acc_check
        else:
            time.sleep(2)
            print(ctypes.windll.user32.GetForegroundWindow())

if __name__ == '__main__':
    print_count()
