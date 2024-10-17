from threading import Thread

import gi
import requests

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from aucd.auc.client.daemon_conn import get_updates
from aucp.auc.prompt.prompt_thread import PromptThread


class PromptWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._updates_list = None
        self._update_label = None
        self._grid = Gtk.Grid()
        self.set_child(self._grid)
        self._label = Gtk.Label()
        self._grid.attach(self._label, 0, 0, 2, 1)

        prompter = PromptThread(self, self._label)
        pt = Thread(target=prompter.prompt_loop, daemon=True)
        pt.start()

    def set_uw(self, text):
        self._label.set_markup(f'<big>{text}</big>')
        self._update_label = Gtk.Label()
        self._update_label.set_markup('<big>Updates Installed:</big>')
        self._grid.attach(self._update_label, 0, 1, 1, 1)
        self._updates_list = Gtk.ListBox()
        self._grid.attach(self._updates_list, 0, 2, 1, 6)
        self.set_updates()

    def set_updates(self):
        try:
            r = get_updates()
            if r.status_code == 200:
                for k, v in r.json()['updates'].items():
                    label = Gtk.Label()
                    label.set_markup('%s from %s to %s' % (k, v['old'], v['new']))
                    row = Gtk.ListBoxRow()
                    row.set_child(label)
                    self._updates_list.append(row)
            elif 'error' in r.json():
                label = Gtk.Label(r.json()['error'])
                label.set_markup(r.json()['error'])
                row = Gtk.ListBoxRow()
                row.set_child(label)
                self._updates_list.append(row)
            else:
                label = Gtk.Label()
                label.set_markup('ERR: Unknown error getting status')
                row = Gtk.ListBoxRow()
                row.set_child(label)
                self._updates_list.append(row)
        except requests.exceptions.RequestException:
            label = Gtk.Label()
            label.set_markup('Could not connect to aucd')
            row = Gtk.ListBoxRow()
            row.set_child(label)
            self._updates_list.append(row)
