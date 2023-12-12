import gi
import requests

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk

from auc.client.daemon_conn import get_status, get_updates


class UpdatesWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid = Gtk.Grid()
        self.set_child(self._grid)
        self._status_label = Gtk.Label()
        self._set_status()
        self._grid.attach(self._status_label, 0, 0, 1, 1)
        self._update_label = Gtk.Label()
        self._update_label.set_markup('<big>Updates Installed:</big>')
        self._grid.attach(self._update_label, 0, 1, 1, 1)
        self._updates_list = Gtk.ListBox()
        self._grid.attach(self._updates_list, 0, 2, 1, 6)
        self._get_updates()

    def _set_status(self):
        try:
            s = get_status()
            if s.status_code == 200:
                self._status_label.set_markup(f'<big>{s.json()["status"]}</big>')
            elif 'error' in s.json():
                self._status_label.set_markup(f'<big>{s.json()["error"]}</big>')
            else:
                self._status_label.set_markup('<big>ERR: Unknown error getting status</big>')
        except requests.exceptions.RequestException:
            self._status_label.set_markup('<big>Could not connect to aucd</big>')

    def _get_updates(self):
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
