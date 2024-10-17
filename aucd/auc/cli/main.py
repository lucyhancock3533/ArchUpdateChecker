import json
import logging
import sys
from argparse import ArgumentParser

import requests_unixsocket

from aucd.auc.client.daemon_conn import get_status, get_updates, set_no_reboot, set_update, set_run, connect_listener, set_mirrorlist
from aucd.auc.client.log_conn import LogListener

log_levels = {'error': logging.ERROR, 'warning': logging.WARNING, 'info': logging.INFO, 'debug': logging.DEBUG}


def version(logger):
    logger.info('AUC v1.4.0')


def load_secret(logger):
    try:
        with open('/tmp/.auc_secret', 'r') as f:
            secret = f.read()
        return secret
    except PermissionError:
        logger.error('No permissions to read AUC secret')
        exit(1)


def status_cmd(logger):
    r = get_status()
    if r.status_code == 200:
        logger.info(r.json()['status'])
    elif 'error' in r.json():
        logger.error(r.json()['error'])
    else:
        logger.error('Unknown error')


def clear_reboot(logger):
    secret = load_secret(logger)
    r = set_no_reboot(secret)
    if r.status_code == 200:
        logger.info(r.json()['msg'])
    elif 'error' in r.json():
        logger.error(r.json()['error'])
    else:
        logger.error('Unknown error')


def updates_cmd(logger):
    r = get_updates()
    if r.status_code == 200:
        for k, v in r.json()['updates'].items():
            logger.info('%s from %s to %s' % (k, v['old'], v['new']))
    elif 'error' in r.json():
        logger.error(r.json()['error'])
    else:
        logger.error('Unknown error')


def do_updates(logger):
    secret = load_secret(logger)
    listener = LogListener()
    r = connect_listener(secret, listener.socket_path)
    if r.status_code == 200:
        if r.json()['success']:
            logging.debug('Connected aucd logger')
    elif 'error' in r.json():
        logger.error(r.json()['error'])
        return
    else:
        logger.error('Unknown error')
        return
    conn = listener.get_connection()
    r = set_update(secret)
    if r.status_code == 200:
        if r.json()['success']:
            logging.debug('Set update flag')
    elif 'error' in r.json():
        logger.error(r.json()['error'])
        return
    else:
        logger.error('Unknown error')
        return
    r = set_run(secret)
    if r.status_code == 200:
        if r.json()['success']:
            logging.debug('Set run flag')
    elif 'error' in r.json():
        logger.error(r.json()['error'])
        return
    else:
        logger.error('Unknown error')
        return

    log_watcher(logger, listener, conn)


def do_mirrorlist(logger):
    secret = load_secret(logger)
    listener = LogListener()
    r = connect_listener(secret, listener.socket_path)
    if r.status_code == 200:
        if r.json()['success']:
            logging.debug('Connected aucd logger')
    elif 'error' in r.json():
        logger.error(r.json()['error'])
        return
    else:
        logger.error('Unknown error')
        return
    conn = listener.get_connection()
    r = set_mirrorlist(secret)
    if r.status_code == 200:
        if r.json()['success']:
            logging.debug('Set mirrorlist flag')
    elif 'error' in r.json():
        logger.error(r.json()['error'])
        return
    else:
        logger.error('Unknown error')
        return
    r = set_run(secret)
    if r.status_code == 200:
        if r.json()['success']:
            logging.debug('Set run flag')
    elif 'error' in r.json():
        logger.error(r.json()['error'])
        return
    else:
        logger.error('Unknown error')
        return

    log_watcher(logger, listener, conn)


def connect_logger(logger):
    secret = load_secret(logger)
    listener = LogListener()
    r = connect_listener(secret, listener.socket_path)
    if r.status_code == 200:
        if r.json()['success']:
            logging.debug('Connected aucd logger')
    elif 'error' in r.json():
        logger.error(r.json()['error'])
        return
    else:
        logger.error('Unknown error')
        return
    conn = listener.get_connection()

    log_watcher(logger, listener,conn)


def log_watcher(logger, listener, conn):
    logger.info('Connected to aucd')
    try:
        while True:
            d = json.loads(conn.recv_bytes().decode())
            if d['msg'] is not None:
                if '{ENDWATCH}' in d['msg']:
                    conn.close()
                    listener.close_socket()
                    break
                if '[LISTENER]' not in d['msg']:
                    logger.info(d['msg'])
    except (EOFError, KeyboardInterrupt):
        conn.close()
        listener.close_socket()
        exit(0)


def add_parser():
    parser = ArgumentParser()
    parser.add_argument('--log-level', type=str, default='info', nargs='?', choices=log_levels.keys())
    parser.add_argument('clicmd', type=str, choices=cmds.keys())
    return parser.parse_args()


def run_cli(args, logger):
    requests_unixsocket.monkeypatch()
    cmds[args.clicmd](logger)


def run():
    args = add_parser()

    log_format = '[AUC] [%(levelname)s] %(message)s'
    logging.basicConfig(level=log_levels[args.log_level],
                        handlers=[logging.StreamHandler(sys.stdout)],
                        format=log_format)
    logger = logging.getLogger(name="auc")

    run_cli(args, logger)


cmds = {
    'status': status_cmd,
    'updates': updates_cmd,
    'clear-reboot':  clear_reboot,
    'update': do_updates,
    'ml': do_mirrorlist,
    'watch': connect_logger
}

if __name__ == '__main__':
    run()
