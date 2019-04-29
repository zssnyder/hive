#imports gi,gtk 3.0
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

import threading, queue
from UI import UI
#from hive.core.mesh import mesh
#from hive.core.swarm import swarm

class UIThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("UI init")
    
    def run(self):
        global interface
        interface.startUI()

logQueue = queue.Queue()
droneQueue = queue.Queue()
commandQueue = queue.Queue()
handlerQueue = queue.Queue()
interface = UI.InitializeUI(logQueue,droneQueue,commandQueue,handlerQueue)
uithread = UIThread()
uithread.start()
logQueue.put("Drone 1 Connected.")
logQueue.put("Drone 2 Connected.")
logQueue.put("Drone 3 Connected.")
logQueue.put("Drone 4 Connected.")
logQueue.put("Drone 5 Connected.")
logQueue.put("All Drones Connected.")
logQueue.put("Preset U Selected.")

