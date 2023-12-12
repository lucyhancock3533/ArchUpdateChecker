from threading import Thread

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk

from auc.prompt.prompt_thread import PromptThread


class PromptWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid = Gtk.Grid()
        self.set_child(self._grid)
        self._label = Gtk.Label()
        self._grid.attach(self._label, 0, 0, 2, 1)

        prompter = PromptThread(self._label)
        pt = Thread(target=prompter.prompt_loop, daemon=True)
        pt.start()
