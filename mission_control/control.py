import backendexample as backend
import threading

class UIThread(threading.Thread):
    def __init__(self):
        exec(open("mission_control/backendexample.py").read())




uithread = UIThread()
uithread.start()