#! /usr/bin/python3
"""AUC Main module, syncs, checks for updates, and alerts user."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from aucgtk import MirrorlistSettingsWindow, run_auc
from aucpmml import get_mrl_url

if(__name__ == "__main__"):
    mirrorlist = get_mrl_url()
    if(mirrorlist == ""): # If mirrorlist url not set, prompt
        mlget = MirrorlistSettingsWindow()
        mlget.connect("delete-event", Gtk.main_quit)
        mlget.show_all()
        Gtk.main()
    else:
        if(run_auc()):
            Gtk.main()
