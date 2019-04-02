import backendexample as backend
import threading

class UIThread(threading.Thread):
    def __init__(self):
        self.runFile()

    def runFile(self):
        fileStream = open("mission_control/backendexample.py").read()
        script = compile(fileStream,"mission_control/backendexample.py","exec")
        exec(script)

uithread = UIThread()
uithread.start()