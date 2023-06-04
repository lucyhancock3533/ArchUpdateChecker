#! /usr/bin/python3
"""AUC Main module, syncs, checks for updates, and alerts user."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from aucgtk import UpdateNotificationWindow, MirrorlistSettingsWindow
from aucpacman import getUpdateCount, syncDB
from aucpmml import getMrlUrl

def run_auc():
    # update mirrorlist here
    syncDB() # Update pacman database
    if (getUpdateCount() > 0):
        notify = UpdateNotificationWindow("<big>" + str(getUpdateCount()) + " updates are available</big>") # Alert user to updates
        notify.connect("delete-event", Gtk.main_quit)
        notify.show_all()
        return True
    else:
        return False

mirrorlist = getMrlUrl()
if(mirrorlist == ""): # If mirrorlist url not set, prompt
    mlget = MirrorlistSettingsWindow()
    mlget.connect("delete-event", Gtk.main_quit)
    mlget.show_all()
    Gtk.main()
else:
    if(run_auc()):
        Gtk.main()
