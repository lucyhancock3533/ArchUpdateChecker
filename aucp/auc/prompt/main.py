import sys

import requests_unixsocket
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw

from aucp.auc.prompt.prompt_window import PromptWindow


class AucGtkApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.window = None

    def on_activate(self, app):
        self.window = PromptWindow(application=app, title='AUC')
        self.window.present()


def run():
    requests_unixsocket.monkeypatch()
    app = AucGtkApp(application_id="dev.leh.auc")
    sys.exit(app.run(sys.argv))


if __name__ == '__main__':
    run()
