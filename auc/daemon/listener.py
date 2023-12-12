import secrets

from pathlib import Path
from multiprocessing.connection import Listener


class DaemonListener:
    def __init__(self, args, logger):
        self.args = args
        self.logger = logger
        self._init_secret()
        Path('/tmp/.auc_socket').unlink(missing_ok=True)
        self.listener = Listener('/tmp/.auc_socket', family='AF_UNIX', authkey=self.secret.encode())

    def _init_secret(self):
        self.secret = secrets.token_hex(nbytes=512)
        Path('/tmp/.auc_secret').unlink(missing_ok=True)
        with open('/tmp/.auc_secret', 'w') as f:
            f.write(self.secret)

    def listen_loop(self):
        try:
            self.logger.info('Starting daemon listener')
            while True:
                conn = self.listener.accept()
                while True:
                    try:
                        msg = conn.recv()
                        print(msg)
                        conn.send('recv')
                    except EOFError:
                        conn.close()
                        break
        except KeyboardInterrupt:
            self.listener.close()
            Path('/tmp/.auc_socket').unlink(missing_ok=True)
            Path('/tmp/.auc_secret').unlink(missing_ok=True)
            self.logger.info('Exiting')

