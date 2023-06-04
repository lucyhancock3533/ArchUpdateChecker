#! /usr/bin/python3
"""AUC Main module, syncs, checks for updates, and alerts user."""

from sys import argv
from auccli import run_auc_cli

if(__name__ == "__main__"):
    if(len(argv) > 1):
        run_auc_cli()
    else:
        try:
            import gi
            gi.require_version('Gtk', '3.0')
            from aucgtk import run_auc_gtk
            run_auc_gtk()
        except ImportError:
            print("[AUC] GTK not available and no parameters passed")
