from threading import Lock


class AucState:
    def __init__(self, config=None):
        self.lock = Lock()
        self.state = {
            'msg': 'Waiting',
            'prompt': False,
            'mirrorlist': True,
            'update': True,
            'inprogress': True,
            'rebootrequired': False,
            'updateneeded': True,
            'updates': {}
        }

        if config is not None:
            self.state['update'] = config.update_on_start

    def access_state(self, key):
        self.lock.acquire()
        v = self.state[key]
        self.lock.release()
        return v

    def set_state(self, key, val):
        self.lock.acquire()
        self.state[key] = val
        self.lock.release()
