import uuid
import secrets

from pathlib import Path
from multiprocessing.connection import Listener


class LogListener:
    def __init__(self):
        self._socket_id = str(uuid.uuid4())
        self._secret = secrets.token_hex(nbytes=1024)
        self._create_socket()

    def _create_socket(self):
        self._socket_path = f'/tmp/.auc_{self._socket_id}'
        self._socket = Listener(self._socket_path, family='AF_UNIX', authkey=self._secret.encode())
        Path(self._socket_path).chmod(0o777)

    def get_connection(self):
        return self._socket.accept()

    def close_socket(self):
        self._socket.close()
        Path(self._socket_path).unlink()

    @property
    def secret(self):
        return self._secret

    @property
    def socket_id(self):
        return self._socket_id

    @property
    def socket_path(self):
        return self._socket_path

    @property
    def socket(self):
        return self._socket
