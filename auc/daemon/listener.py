import secrets

from pathlib import Path
from multiprocessing.connection import Listener


class DaemonListener:
    def __init__(self, args, logger, state):
        self.args = args
        self.logger = logger
        self.state = state
        self._init_secret()
        Path('/tmp/.auc_socket').unlink(missing_ok=True)
        self.listener = Listener('/tmp/.auc_socket', family='AF_UNIX', authkey=self.secret.encode())

    def _init_secret(self):
        self.secret = secrets.token_hex(nbytes=512)
        Path('/tmp/.auc_secret').unlink(missing_ok=True)
        with open('/tmp/.auc_secret', 'w') as f:
            f.write(self.secret)

    def listen_loop(self):
        self.logger.info('[LISTENER] Starting daemon listener')
        while True:
            conn = self.listener.accept()
            while True:
                self.logger.debug("[LISTENER] New connection accepted")
                try:
                    msg = conn.recv()
                    if msg not in func.keys():
                        self.logger.error('[LISTENER] Requested operation from client not valid')
                        conn.send('err:notvalid')
                    else:
                        self.logger.info('[LISTENER] Executing %s' % msg)
                        conn.send(func[msg](self.state))
                except EOFError:
                    conn.close()
                    break


def get_status(state):
    return state.access_state('msg')


def get_prompt(state):
    if state.access_state('prompt'):
        return state.access_state('msg')
    return 'err:inprogress'


func = {'status': get_status, 'prompt': get_prompt}
