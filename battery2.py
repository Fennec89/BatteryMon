import os
import time
import re
import pygtk
pygtk.require('2.0')
import gtk
from threading import Timer


class StatusIcon:
    def __init__(self):
        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_file("/home/gustav/Dev/Python/BatteryMon/icon.png")
        #self.statusicon.connect("popup-menu", self.right_click_event)
        self.statusicon.set_tooltip("StatusIcon Example")
        
        window = gtk.Window()
        window.connect("destroy", lambda w: gtk.main_quit())
        #window.show_all()

StatusIcon()
gtk.main()
