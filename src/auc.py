#! /usr/bin/python3
"""AUC Main module, syncs, checks for updates, and alerts user."""

import gi
#import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from aucgtk import UpdateNotificationWindow
from aucpacman import getUpdateCount, syncDB

mirrorlistAddress = "https://www.archlinux.org/mirrorlist/?country=all&protocol=http&protocol=https&ip_version=4&ip_version=6&use_mirror_status=on" # Address of mirrorlist to fetch

#mlp = subprocess.Popen(["/usr/bin/gksudo", "/usr/bin/wget -O /etc/pacman.d/mirrorlist \"" + mirrorlistAddress + "\""]) # Update pacman mirrorlist
#mlp.wait()
#mlr = subprocess.Popen(["/usr/bin/gksudo", "/usr/bin/sed -i 's/#S/S/g' /etc/pacman.d/mirrorlist"]) # Replace #S on auto-generated mirrorlist
#mlr.wait()
syncDB() # Update pacman database
if (getUpdateCount() > 0):
    notify = UpdateNotificationWindow("<big>" + str(getUpdateCount()) + " updates are available</big>") # Alert user to updates
    notify.connect("delete-event", Gtk.main_quit)
    notify.show_all()
    Gtk.main()
