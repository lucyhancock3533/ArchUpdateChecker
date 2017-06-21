#! /usr/bin/python3

from gi.repository import Gtk
from aucpacman import getUpdates

class UpdateNotificationDialog(Gtk.Window): # Dialog for displaying message to user
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
        window = UpdateViewWindow(getUpdates())
        window.show_all()

    def launchUpdateWindow(self, button):
        window = UpdateStatusWindow()
        window.show_all()

class UpdateViewWindow(Gtk.Window):
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
    def __init__(self):
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
