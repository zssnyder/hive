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
    def __init__(self,q):
        global builder
        self.logQ = q
        self.status1 = builder.get_object("status1")
        self.status2 = builder.get_object("status2")
        self.status3 = builder.get_object("status3")
        self.status4 = builder.get_object("status4")
        self.status5 = builder.get_object("status5")

        self.source = GObject.timeout_add(1000,self.readQueue,self.logQ)

        style_provider = Gtk.CssProvider()

        css = open('mission_control/UI/Default.css', 'rb') # rb needed for python 3 support
        css_data = css.read()
        css.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def writeToStatus(self,textbuff,sts,x,y,z,bat):
        textbuff.set_text("Status: "+sts+"\n"+"X: "+x+"\n"+"Y: "+y+"\n"+"Z: "+z+"\n"+"Bat: "+bat)

    def hideStatus(self):
        self.status1.hide()
        self.status2.hide()
        self.status3.hide()
        self.status4.hide()
        self.status5.hide()
    
    def allDrones_clicked(self, button):
        self.status1.show()
        self.status2.show()
        self.status3.show()
        self.status4.show()
        self.status5.show()

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

    def theme0_activate(self, button):
        style_provider = Gtk.CssProvider()

        css = open('mission_control/UI/Default.css', 'rb') # rb needed for python 3 support
        css_data = css.read()
        css.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def theme1_activate(self, button):
        style_provider = Gtk.CssProvider()

        css = open('mission_control/UI/Light.css', 'rb') # rb needed for python 3 support
        css_data = css.read()
        css.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def theme2_activate(self, button):
        style_provider = Gtk.CssProvider()

        css = open('mission_control/UI/Dark.css', 'rb') # rb needed for python 3 support
        css_data = css.read()
        css.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    def onWindowDestroy(self, *args):
        Gtk.main_quit()

    def onQuitClicked(self,button):
        Gtk.main_quit()

    def insertText(self,text):
        textBuffer = builder.get_object("DataLog")
        endBuffer = textBuffer.get_end_iter()
        textBuffer.insert(endBuffer,"\n"+text)

    def readQueue(self,q):
        text = None
        if not q.empty():
           text = q.get(True,1)
           q.task_done()
        if not text is None:
            self.insertText(text)
        return True
#=======================================================
class InitializeUI():
    def __init__(self,logQueue):
        global builder
        global window
        self.logQ = logQueue
        self.hand = Handler(self.logQ)
        #connect signals from .glade file to event handlers.
        #For this to work the signals must have the name of the event handler in the "handler" field in glade.
        builder.connect_signals(self.hand)
        #Runs the gtk main method, which renders out the UI and waits for user input.
        window.show()
        self.hand.hideStatus()

    def startUI(self):
        Gtk.main()
    
    def addToQueue(self,objToAdd):
        self.logQ.put(objToAdd,True,1)

#create builder object
builder = Gtk.Builder()
#Add the .glade file to the builder.
builder.add_from_file("mission_control/UI/UI.glade")
#objects can be created to manipulate UI elements.
window = builder.get_object("Swarm_Control")
