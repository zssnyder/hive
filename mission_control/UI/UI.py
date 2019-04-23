#imports gi,gtk 3.0
import gi,queue,threading,cairo
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

#=======================================================
#The handler class listens for signals from the UI.
#Each method in the class is an event handler.
class Handler:
    def __init__(self,lq,dq,cq,hq):
        global builder
        self.logQ = lq
        self.droneQ = dq
        self.commandQ = cq
        self.handlerQ = hq
        self.status1 = builder.get_object("status1")
        self.status2 = builder.get_object("status2")
        self.status3 = builder.get_object("status3")
        self.status4 = builder.get_object("status4")
        self.status5 = builder.get_object("status5")

        self.allStat = True

        self.source = GObject.timeout_add(1000,self.readQueue,self.logQ)

        style_provider = Gtk.CssProvider()

        css = open('mission_control/UI/theme_config.css', 'rb') # rb needed for python 3 support
        css_data = css.read()
        css.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.initTracking()

    def initTracking(self):
        global builder
        self.dwa = builder.get_object("DroneTracking")
        self.dwa.queue_draw()

    def onDroneTacking_draw(self, widget, event):
        cr = widget.window.cario_create()
        
        cr.set_source_rgb(1,0,1)
        cr.rectangle(20, 20, 120, 80)
        cr.rectangle(180, 20, 80, 80)
        
        cr.fill()

    def writeToStatus(self,textbuff,sts,x,y,z,bat):
        textbuff.set_text("Status: "+sts+"\n"+"X: "+x+"\n"+"Y: "+y+"\n"+"Z: "+z+"\n"+"Bat: "+bat)

    def hideStatus(self):
        self.status1.hide()
        self.status2.hide()
        self.status3.hide()
        self.status4.hide()
        self.status5.hide()
    
    def allDrones_clicked(self, button):
        if(self.allStat):
            self.status1.show()
            self.status2.show()
            self.status3.show()
            self.status4.show()
            self.status5.show()
            self.allStat = False
        else:
            self.hideStatus()
            self.allStat = True

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

    def pre1_clicked(self, button):
        self.logQ.put("Preset 1 selected.",True,1)

    def pre2_clicked(self, button):
        self.logQ.put("Preset 2 selected.",True,1)

    def pre3_clicked(self, button):
        self.logQ.put("Preset 3 selected.",True,1)

    def pre4_clicked(self, button):
        self.logQ.put("Preset 4 selected.",True,1)

    def LaunchBtn_clicked(self, button):
        self.logQ.put("Launch initiated.",True,1)

    def theme0_activate(self, button):
        style_provider = Gtk.CssProvider()

        css = open('mission_control/UI/Default.css', 'rb') # rb needed for python 3 support
        css_data = css.read()
        with open('mission_control/UI/Default.css', 'r') as theme_select:
            with open('mission_control/UI/theme_config.css', 'w') as theme_prev:
                for line in theme_select:
                    theme_prev.write(line)
        css.close()
        theme_prev.close()
                
        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def theme1_activate(self, button):
        style_provider = Gtk.CssProvider()

        css = open('mission_control/UI/Light.css', 'rb') # rb needed for python 3 support
        css_data = css.read()
        with open('mission_control/UI/Light.css', 'r') as theme_select:
            with open('mission_control/UI/theme_config.css', 'w') as theme_prev:
                for line in theme_select:
                    theme_prev.write(line)
        css.close()
        theme_prev.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def theme2_activate(self, button):
        style_provider = Gtk.CssProvider()

        css = open('mission_control/UI/Dark.css', 'rb') # rb needed for python 3 support
        css_data = css.read()
        with open('mission_control/UI/Dark.css', 'r') as theme_select:
            with open('mission_control/UI/theme_config.css', 'w') as theme_prev:
                for line in theme_select:
                    theme_prev.write(line)
        css.close()
        theme_prev.close()

        style_provider.load_from_data(css_data)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,     
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    def aboutMenuItem_activate(self, button):
        aboutWindow.show()

    def aboutButton_clicked(self, button):
        if button.get_label() == "Close":
            window = builder.get_object("aboutdialog_Swarm")
            window.destroy()

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
    def __init__(self,logQueue,droneQueue,commandQueue,handlerQueue):
        global builder
        global window
        global aboutWindow
        self.logQ = logQueue
        self.droneQ = droneQueue
        self.commandQ = commandQueue
        self.handQ = handlerQueue
        self.hand = Handler(self.logQ,self.droneQ,self.commandQ,self.handQ)
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
aboutWindow = builder.get_object("aboutdialog_Swarm")
