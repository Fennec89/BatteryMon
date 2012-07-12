#/usr/bin/python2.7
# -*- coding: utf8 -*-
"""
Author: Gustav Fahlén
This script keeps track of the computer battery state and displays it
in a system tray.

I developed this script because i could not find any battery monitor i found nice :)

ToDo:
    Fix better icons [x]
    mouse-over percentage for icon []

"""
import os
import time
import re
import pygtk
pygtk.require('2.0')
import gtk
import gobject
from threading import Timer

class StatusIcon:
    def __init__(self):
        self.statusicon = gtk.StatusIcon()
        self.update()
        self.statusicon.connect("popup-menu", self.right_click_event)
        gobject.timeout_add(3000, self.update)

        window = gtk.Window()
        window.connect("destroy", lambda w: gtk.main_quit())
        #window.show_all()

    def right_click_event(self, icon, button, time):
        menu = gtk.Menu()

        levels = gtk.MenuItem("Levels")
        about = gtk.MenuItem("About")
        quit = gtk.MenuItem("Quit")

        levels.connect("activate", self.show_levels)
        about.connect("activate", self.show_about_dialog)
        quit.connect("activate", gtk.main_quit)

        menu.append(levels)
        menu.append(about)
        menu.append(quit)

        menu.show_all()

        menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Battery status widget")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["Gustav Fahlen"])

        about_dialog.run()
        about_dialog.destroy()

    def show_levels(self, widget):

        temp = self.readAcpi()

        state = temp[0]
        battery = temp[1]

        state_text = gtk.Label(state)
        battery_text = gtk.Label(battery)
        levels = gtk.Dialog("Battery levels")
        levels.add_button("Close", 111)
        levels.vbox.pack_start(state_text)
        levels.vbox.pack_start(battery_text)
        state_text.show()
        battery_text.show()

        levels.run()
        levels.destroy()

    def readAcpi(self):

        values = []
        p = os.popen('acpi -b')

        for line in p.readlines():
            values.append(line)

        return self.parseAcpi(values)

    def parseAcpi(sefl, list):

        battery_info = []
        temp = []

        for element in list:
            temp = element.split(" ")
            battery_info.append(temp[2])
            battery_info.append(temp[3])
        return battery_info
    def setIcon(self, status):
        state = status[0].strip(',')
        current = re.sub("[^0-9]", "", status[1])
        print status
        print state
        print current
        if state == "Discharging":
            if int(current) < 100 and int(current) > 90:
                self.statusicon.set_from_file("/home/gustav/Dev/Python/BatteryMon/icons/battery_full.png")
            elif int(current) < 90 and int(current) > 75:
                self.statusicon.set_from_file("/home/gustav/Dev/Python/BatteryMon/icons/battery_third_fouth.png")
            elif int(current) < 75 and int(current) > 50:
                self.statusicon.set_from_file("/home/gustav/Dev/Python/BatteryMon/icons/battery_two_thirds.png")
            elif int(current) < 50 and int(current) > 15:
                self.statusicon.set_from_file("/home/gustav/Dev/Python/BatteryMon/icons/battery_low.png")
            elif int(current) < 15 and int(current) > 5:
                self.statusicon.set_from_file("/home/gustav/Dev/Python/BatteryMon/icons/battery_caution.png")
            elif int(current) < 5 and int(current) > 0:
                self.statusicon.set_from_file("/home/gustav/Dev/Python/BatteryMon/icons/battery-000.png")
        elif state == "Charging":
            self.statusicon.set_from_file("/home/gustav/Dev/Python/BatteryMon/icons/battery_charged.png")

    def update(self):
        print "Updating ACPI information"
        info = self.readAcpi()
        #time.sleep(5)
        self.setIcon(info)
        return True

StatusIcon()
gtk.main()
