#imports gi,gtk 3.0
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#=======================================================
#The handler class listens for signals from the UI.
#Each method in the class is an event handler.
class Handler:


    def drone1_clicked(self, button):
        builder = Gtk.Builder()
        status1 = builder.get_object("status1")
        status1.set_visible("false")

#Best practices: Name event handlers starting with 'on'.
# Then the name of the control that is signalling.
# Last is the name of the signal. i.e. onButtonClicked





#=======================================================
#create builder object.
builder = Gtk.Builder()
#Add the .glade file to the builder.
builder.add_from_file("mission_control/UI.glade")
#objects can be created to manipulate UI elements.
window = builder.get_object("Swarm Control")
#connect signals from .glade file to event handlers.
#For this to work the signals must have the name of the event handler in the "handler" field in glade.
builder.connect_signals(Handler())
#Runs the gtk main method, which renders out the UI and waits for user input.

window.show_all()
Gtk.main()

