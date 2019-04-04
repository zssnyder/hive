#imports gi,gtk 3.0
import gi,queue
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

#=======================================================
#The handler class listens for signals from the UI.
#Each method in the class is an event handler.
class Handler:
    logQueue = queue.Queue()
    def __init__(self):
        global builder
        self.status1 = builder.get_object("status1")
        self.status2 = builder.get_object("status2")
        self.status3 = builder.get_object("status3")
        self.status4 = builder.get_object("status4")
        self.status5 = builder.get_object("status5")

        source = GObject.timeout_add(10000,self.readQueue,self.logQueue)

        style_provider = Gtk.CssProvider()

        css = open('mission_control/Default.css', 'rb') # rb needed for python 3 support
        css_data = css.read()
        css.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def hideStatus(self):
        self.status1.hide()
        self.status2.hide()
        self.status3.hide()
        self.status4.hide()
        self.status5.hide()

    def drone1_clicked(self, button):     
        if(self.status1.get_visible()):
            self.status1.hide()
        else:
            self.status1.show()

    def drone2_clicked(self, button):     
        if(self.status2.get_visible()):
            self.status2.hide()
        else:
            self.status2.show()

    def drone3_clicked(self, button):     
        if(self.status3.get_visible()):
            self.status3.hide()
        else:
            self.status3.show()

    def drone4_clicked(self, button):     
        if(self.status4.get_visible()):
            self.status4.hide()
        else:
            self.status4.show()

    def drone5_clicked(self, button):     
        if(self.status5.get_visible()):
            self.status5.hide()
        else:
            self.status5.show()
    
    def onWindowDestroy(self, *args):
        Gtk.main_quit()

    def onQuitClicked(self,button):
        Gtk.main_quit()

    def insertText(text):
        print("test")
        textBuffer = builder.get_object("DataLog")
        endBuffer = textBuffer.get_end_iter()
        textBuffer.insert(endBuffer,"\n"+text)

    def readQueue(self,q):
        text = q.get(True,0.1)
        print("test")
        if text is None:
            self.insertText(text)
#=======================================================
class InitializeUI():
    def __init__(self):
        global builder
        global window
        #connect signals from .glade file to event handlers.
        #For this to work the signals must have the name of the event handler in the "handler" field in glade.
        builder.connect_signals(Handler())
        #Runs the gtk main method, which renders out the UI and waits for user input.
        window.show_all()
        Handler.hideStatus(Handler())

    def startUI(self):
        Gtk.main()
    
    def addToQueue(self,objToAdd,q):
        q.put(objToAdd,True,1)

#create builder object
builder = Gtk.Builder()
#Add the .glade file to the builder.
builder.add_from_file("mission_control/UI.glade")
#objects can be created to manipulate UI elements.
window = builder.get_object("Swarm_Control")
