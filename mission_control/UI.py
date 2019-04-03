#imports gi,gtk 3.0
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

#=======================================================
#The handler class listens for signals from the UI.
#Each method in the class is an event handler.
class Handler:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.status1 = self.builder.get_object("status1")
        self.status2 = self.builder.get_object("status2")
        self.status3 = self.builder.get_object("status3")
        self.status4 = self.builder.get_object("status4")
        self.status5 = self.builder.get_object("status5")

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
    

#Best practices: Name event handlers starting with 'on'.
# Then the name of the control that is signalling.
# Last is the name of the signal. i.e. onButtonClicked





#=======================================================
class UI():
    def __init__(self):
        #create builder object.
        self.builder = Gtk.Builder()
        #Add the .glade file to the builder.
        self.builder.add_from_file("mission_control/UI.glade")
        #objects can be created to manipulate UI elements.
        self.window = self.builder.get_object("Swarm_Control")
        #connect signals from .glade file to event handlers.
        #For this to work the signals must have the name of the event handler in the "handler" field in glade.
        self.builder.connect_signals(Handler())
        #Runs the gtk main method, which renders out the UI and waits for user input.

        self.window.show_all()
        Handler.hideStatus(Handler())
        self.Gtk.main()

