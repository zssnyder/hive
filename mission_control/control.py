#imports gi,gtk 3.0
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

import threading
import UI

class UIThread(threading.Thread):
    def __init__(self):
        UI.UI()

    def runFile(self):
        fileStream = open("mission_control/backendexample.py").read()
        script = compile(fileStream,"mission_control/backendexample.py","exec")
        exec(script)

uithread = UIThread()
uithread.start()