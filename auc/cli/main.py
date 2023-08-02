import logging
import sys
from argparse import ArgumentParser

import requests
import requests_unixsocket

from auc.client.daemon_conn import get_status, get_updates

log_levels = {'error': logging.ERROR, 'warning': logging.WARNING, 'info': logging.INFO, 'debug': logging.DEBUG}


def version(logger):
    logger.info('AUC v1.3.1')


def status_cmd(logger):
    r = get_status()
    if r.status_code == 200:
        logger.info(r.json()['status'])
    elif 'error' in r.json():
        logger.error(r.json()['error'])
    else:
        logger.error('Unknown error')


def clear_reboot(logger):
    r = requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'clear-reboot'})
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


cmds = {'status': status_cmd, 'updates': updates_cmd, 'clear-reboot':  clear_reboot}

if __name__ == '__main__':
    run()
