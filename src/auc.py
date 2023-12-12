#! /usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from aucgtk import NotificationDialog
from aucpacman import getUpdateCount, syncDB

syncDB() # Update pacman database
if (getUpdateCount() > 0): # Check for updates
    notify = NotificationDialog("<big>" + str(getUpdateCount()) + " updates are available</big>") # Alert user to updates
    notify.connect("delete-event", Gtk.main_quit)
    notify.show_all()
    Gtk.main()
