#! /usr/bin/python3
"""Module for dealing with GUIs"""

import os
import threading
from gi.repository import GLib, Gtk, GObject
from aucpacman import getUpdates, runUpdates
from subprocess import CalledProcessError
from pathlib import Path
from datetime import datetime
from aucpmml import setMrlUrl
from auc import run_auc

class MessageNotificationWindow(Gtk.Window):
    """Window for displaying message to user"""
    def __init__(self, text):
        Gtk.Window.__init__(self, title="AUC") # Create window
        grid = Gtk.Grid() # Create component grid
        self.add(grid)
        label = Gtk.Label() # Create and set label to input
        label.set_markup(text)
        grid.attach(label, 0, 0, 2, 1)

class UpdateNotificationWindow(Gtk.Window):
    """Window for displaying update message to user"""
    def __init__(self, text):
        Gtk.Window.__init__(self, title="AUC") # Create window
        grid = Gtk.Grid() # Create component grid
        self.add(grid)
        label = Gtk.Label() # Create and set label to input
        label.set_markup(text)
        grid.attach(label, 0, 0, 2, 1)
        updateButton = Gtk.Button("Update") # Add update button
        viewButton = Gtk.Button("View") # Add view updates button
        viewButton.connect("clicked", self.launchViewWindow)
        updateButton.connect("clicked", self.launchUpdateWindow)
        grid.attach(viewButton, 0, 1, 1, 1)
        grid.attach(updateButton, 1, 1, 1, 1)

    def launchViewWindow(self, button):
        try:
            window = UpdateViewWindow(getUpdates())
            window.show_all()
        except CalledProcessError:
            msg = MessageNotificationWindow("<big>No updates available to view</big>")
            msg.show_all()

    def launchUpdateWindow(self, button):
        window = UpdateStatusWindow(self)
        window.show_all()

class UpdateViewWindow(Gtk.Window):
    """Window for viewing available updates"""
    def __init__(self, updates):
        Gtk.Window.__init__(self, title="AUC") # Create window
        listbox = Gtk.ListBox() # Create list of updates
        for update in updates: # Populate update list
            label = Gtk.Label(update.decode("utf-8"))
            row = Gtk.ListBoxRow()
            row.add(label)
            listbox.add(row)
        self.add(listbox)

class UpdateStatusWindow(Gtk.Window):
    """Window for showing update status"""
    def __init__(self, parent):
        Gtk.Window.__init__(self, title="AUC") # Create window
        self.set_default_size(800, 600) # Set window size
        scrolledwindow = Gtk.ScrolledWindow() # Create scrolled container
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.add(scrolledwindow)
        self.textview = Gtk.TextView() # Create text view
        self.textbuffer = self.textview.get_buffer()
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textview.set_wrap_mode(2)
        scrolledwindow.add(self.textview)
        self.updatesthread = threading.Thread(target=self.doUpdates) # Start updates thread
        self.updatesthread.start()
        self.super = parent

    def updateProgress(self, progress):
        self.textbuffer.insert_at_cursor(progress) # Add progress to text view
        self.textview.scroll_to_mark(self.textbuffer.get_insert(), 0.0, True, 0.5, 0.5)

    def finishUpdates(self, parent):
        self.saveLog()
        msg = MessageNotificationWindow("<big>Updates are complete</big>")
        msg.show_all()
        msg.connect("delete-event", Gtk.main_quit)
        self.hide()
        parent.hide()

    def saveLog(self):
        logFolder = Path(os.path.expanduser("~/.auc/"))
        logFolder.mkdir(parents=True, exist_ok=True)
        log = open(os.path.expanduser("~/.auc/") + str(datetime.now()) + ".log", "w")
        log.write(self.textbuffer.get_text(self.textbuffer.get_iter_at_line(0), self.textbuffer.get_iter_at_line(self.textbuffer.get_line_count()), True))
        log.close()

    def doUpdates(self):
        try:
            updates = runUpdates() # Run updates
            for line in updates.stdout: # Update text view
                GLib.idle_add(self.updateProgress, line.decode())
            GLib.idle_add(self.finishUpdates, self.super)
        except CalledProcessError:
            msg = MessageNotificationWindow("<big>Failed to install updates</big>")
            msg.show_all()

class MirrorlistSettingsWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="AUC") #Create Window
        grid = Gtk.Grid()
        self.add(grid) # Create and add grid UI
        label = Gtk.Label("Please input mirrorlist URL")
        grid.attach(label, 0, 0, 2, 1)
        sc_win = Gtk.ScrolledWindow()
        sc_win.set_hexpand(True)
        sc_win.set_vexpand(True)
        grid.attach(sc_win, 0, 1, 2, 2) # Create and add scrolled UI
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer() # Create text view and get buffer
        self.textview.set_wrap_mode(2)
        sc_win.add(self.textview) # Setup and add to sc_win
        save_button = Gtk.Button("Save")
        exit_button = Gtk.Button("Exit")
        save_button.connect("clicked", self.set_mirrorlist)
        exit_button.connect("clicked", Gtk.main_quit)
        grid.attach(save_button, 0, 3, 1, 1)
        grid.attach(exit_button, 1, 3, 1, 1)
    def set_mirrorlist(self, parent):
        setMrlUrl(self.textbuffer.get_text(self.textbuffer.get_iter_at_line(0), self.textbuffer.get_iter_at_line(self.textbuffer.get_line_count()), True))
