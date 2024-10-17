import time

import requests.exceptions

from aucd.auc.client.daemon_conn import get_status, get_prompt


class PromptThread:
    def __init__(self, window, label):
        self._window = window
        self._label = label

    def prompt_loop(self):
        running = True
        while running:
            try:
                p = get_prompt()
                if p.status_code == 200:
                    if 'error' in p.json():
                        if p.json()['error'] == 'notrequired':
                            running = False
                    elif 'prompt' in p.json():
                        self._window.set_uw(p.json()['prompt'])
                        running = False

                s = get_status()
                if s.status_code == 200:
                    self._label.set_markup(f'<big>{s.json()["status"]}</big>')
                elif 'error' in s.json():
                    self._label.set_markup(f'<big>{s.json()["error"]}</big>')
                else:
                    self._label.set_markup('<big>ERR: Unknown error getting status</big>')
            except requests.exceptions.RequestException:
                self._label.set_markup('<big>Could not connect to aucd</big>')

            time.sleep(1)
