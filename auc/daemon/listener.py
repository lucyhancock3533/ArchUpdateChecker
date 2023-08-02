import secrets
import os
import json

from pathlib import Path
from http.server import BaseHTTPRequestHandler

from auc.daemon.util.unix_http import UnixHTTPServer


class AUCRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        req = json.loads(body.decode('UTF-8'))
        if 'function' not in req:
            self.server.logger.error('[LISTENER] Requested operation from client not valid')
            err = {'error': 'Function not specified'}
            self.send_error(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(err).encode('UTF-8'))
            return

        if req['function'] not in func.keys():
            self.server.logger.error('[LISTENER] Requested operation from client not valid')
            err = {'error': f'Invalid function {req["function"]}'}
            self.send_error(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(err).encode('UTF-8'))
            return

        self.server.logger.info('[LISTENER] Executing %s' % req['function'])
        resp = func[req['function']](self.server.state)
        if resp is None:
            err = {'error': 'Function not allowed'}
            self.wfile.write(json.dumps(err).encode('UTF-8'))
            self.send_response(403)
            return
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode('UTF-8'))

    def log_message(self, format, *args):
        message = format % args
        self.server.logger.debug('Request [%s] %s' % (self.log_date_time_string(), message))


class DaemonListener:
    def __init__(self, args, logger, state):
        self.args = args
        self.logger = logger
        self.state = state
        self._init_secret()
        Path('/tmp/.auc_socket').unlink(missing_ok=True)
        self.listener = UnixHTTPServer('/tmp/.auc_socket', AUCRequestHandler, self.state, self.logger, self.secret)
        os.chmod('/tmp/.auc_socket', 0o777)

    def _init_secret(self):
        self.secret = secrets.token_hex(nbytes=512)
        Path('/tmp/.auc_secret').unlink(missing_ok=True)
        with open('/tmp/.auc_secret', 'w') as f:
            f.write(self.secret)
        os.chmod('/tmp/.auc_secret', 0o600)

    def listen_loop(self):
        self.logger.info('[LISTENER] Starting daemon listener')
        self.listener.serve_forever()


def get_status(state):
    return {'status': state.access_state('msg')}


def clear_reboot(state):
    if state.access_state('rebootrequired'):
        state.set_state('rebootrequired', False)
        state.set_state('msg', 'Nothing to do')
        return {'msg': 'Reboot cleared'}
    else:
        return {'msg': 'No reboot required'}


def get_prompt(state):
    if not state.access_state('prompt') and not state.access_state('inprogress'):
        return {'error': 'notrequired'}
    if state.access_state('prompt'):
        return {'prompt': state.access_state('msg')}
    return {'error': 'noprompt'}


def get_updates(state):
    return {'updates': state.access_state('updates')}


func = {'status': get_status, 'prompt': get_prompt, 'updates': get_updates, 'clear-reboot': clear_reboot}
