#! /usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class NotificationDialog(Gtk.Window): # Dialog for displaying message to user
    def __init__(self, text):
        Gtk.Window.__init__(self, title="AUC") # Create window
        box = Gtk.Box(spacing=6) # Create box
        self.add(box)
        label = Gtk.Label() # Create and set label to input
        box.add(label)
        label.set_markup(text)
