#! /usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class UpdateNotificationDialog(Gtk.Window): # Dialog for displaying message to user
    def __init__(self, text):
        Gtk.Window.__init__(self, title="AUC") # Create window
        grid = Gtk.Grid() # Create box
        self.add(grid)
        label = Gtk.Label() # Create and set label to input
        label.set_markup(text)
        grid.attach(label, 0, 0, 2, 1)
        updateButton = Gtk.Button("Update")
        viewButton = Gtk.Button("View")
        grid.attach(viewButton, 0, 1, 1, 1)
        grid.attach(updateButton, 1, 1, 1, 1)

class UpdateStatusWindow(Gtk.Window):
    def __init(self):
        print()
