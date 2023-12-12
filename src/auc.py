#! /usr/bin/python3
"""AUC Main module, syncs, checks for updates, and alerts user."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from aucgtk import run_auc_gtk

if(__name__ == "__main__"):
    run_auc_gtk()
