import secrets

from multiprocessing.connection import Listener


class DaemonListener:
    def __init__(self):
        self._init_secret()
        self.listener = Listener('/tmp/.auc_socket', family='AF_UNIX', authkey=self.secret.encode())

    def _init_secret(self):
        self.secret = secrets.token_hex(nbytes=512)
        with open('/tmp/.auc_secret', 'w') as f:
            f.write(self.secret)

    def listen_loop(self):
        conn = self.listener.accept()
        while True:
            msg = conn.recv()
            print(msg)
