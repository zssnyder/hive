import gi
from gi.repository import Gtk
import math

class PyApp(Gtk.Window):
   
    def __init__(self):
        super(PyApp, self).__init__()
      
        self.set_title("Drone Tracking Test")
        self.set_size_request(500, 500)
        
        self.connect("destroy", Gtk.main_quit)
        
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.expose)
        
        self.add(darea)
        self.show_all()
        
    def expose(self, widget, cr):
        cenx = 250
        ceny = 300

        cr.set_source_rgb(0,0,0)
        cr.set_line_width(2)
        cr.rectangle(0,0,500,500)
        cr.fill()

        cr.set_source_rgb(1,0,0)
        cr.move_to(cenx,ceny)
        cr.line_to(250,0)
        cr.stroke()
        
        cr.set_source_rgb(0,1,0)
        cr.move_to(cenx,ceny)
        cr.line_to(0,500)
        cr.stroke()

        cr.set_source_rgb(0,0,1)
        cr.move_to(cenx,ceny)
        cr.line_to(500,500)
        cr.stroke()

        cr.set_source_rgb(1,0,1)
        cr.move_to(275,350)
        cr.line_to(275,200)
        cr.stroke()
        cr.move_to(270,205)
        cr.line_to(275,200)
        cr.line_to(280,205)
        cr.line_to(270,205)
        cr.fill()

PyApp()
Gtk.main() 