from threading import Lock


class AucState:
    def __init__(self):
        self.lock = Lock()
        self.state = {
            'msg': 'Updates in progress',
            'prompt': False,
            'mirrorlist': True,
            'update': True,
            'inprogress': True,
            'rebootrequired': False,
            'updates': {}
        }

    def access_state(self, key):
        self.lock.acquire()
        v = self.state[key]
        self.lock.release()
        return v

    def set_state(self, key, val):
        self.lock.acquire()
        self.state[key] = val
        self.lock.release()
