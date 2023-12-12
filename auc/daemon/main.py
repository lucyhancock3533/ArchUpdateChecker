import subprocess
import sys
import time
import logging
import requests
from argparse import ArgumentParser

from threading import Thread
from pathlib import Path
from datetime import datetime

from auc.daemon.listener import DaemonListener
from auc.daemon.util.config import AucConfig
from auc.daemon.util.state import AucState
from auc.daemon.mirrorlist import MirrorlistUpdate
from auc.daemon.pacman_updater import PacmanUpdater
from auc.daemon.yay_updater import YayUpdater

log_levels = {'error': logging.ERROR, 'warning': logging.WARNING, 'info': logging.INFO, 'debug': logging.DEBUG}


def add_parser():
    parser = ArgumentParser()
    parser.add_argument('--log-level', type=str, default='info', nargs='?', choices=log_levels.keys())
    parser.add_argument('--config', type=str, default='/etc/auc.yaml', nargs='?')
    return parser.parse_args()


def check_network(ping_addr):
    try:
        requests.get(ping_addr)
        return True
    except requests.exceptions.RequestException:
        return False


def run_daemon(args, logger):
    config = AucConfig(args.config, logger)
    if config.file_log:
        logger.addHandler(logging.FileHandler(f'{config.log_path}/auc_{datetime.today().strftime("%Y-%m-%d")}.log'))
    yay = config.use_yay
    logger.info('Starting AUC daemon')
    state = AucState()
    Path(config.log_path).mkdir(parents=True, exist_ok=True)

    # Start listener thread
    logger.info('Starting listener')
    listener = DaemonListener(args, logger, state)
    lt = Thread(target=listener.listen_loop, daemon=True)
    lt.start()

    try:
        while True:
            logger.debug('Running main loop')
            if state.access_state('inprogress'):
                state.set_state('msg', 'Running updates')
                network = False
                state.set_state('msg', 'Waiting for network connection')
                logger.info('Checking for network connection')
                while not network:
                    network = check_network(config.ping_addr)
                    if not network:
                        time.sleep(15)

                did_something = False
                logger.info('Executing updates')
                state.set_state('msg', 'Updates in progress')

                # Update mirrorlist
                if config.update_mr and state.access_state('mirrorlist'):
                    state.set_state('msg', 'Updating mirrorlist')
                    mrl = MirrorlistUpdate(config.mr_url, logger)
                    res = mrl.update_mirrorlist()
                    if res:
                        state.set_state('mirrorlist', False)
                    else:
                        logger.error('Failed to update mirror list')
                        state.set_state('inprogress', False)
                        state.set_state('prompt', True)
                        state.set_state('msg', 'Failed to update mirror list')
                        logger.critical('{ENDWATCH}')
                        continue

                # Do updates
                if state.access_state('update'):
                    state.set_state('msg', 'Checking for updates')
                    if yay:
                        p = YayUpdater(logger, config.log_path)
                    else:
                        p = PacmanUpdater(logger, config.log_path)
                    logger.info('Updating pacman database')
                    try:
                        p.sync_db()
                    except subprocess.CalledProcessError:
                        logger.error('Failed to check for updates')
                        state.set_state('inprogress', False)
                        state.set_state('prompt', True)
                        state.set_state('msg', 'Failed to sync pacman DB, see logs for more detail')
                        logger.critical('{ENDWATCH}')
                        continue

                    try:
                        updates = p.get_updates()
                        state.set_state('updates', updates)
                    except subprocess.CalledProcessError:
                        logger.info('No updates are available')
                        updates = {}

                    if len(updates.keys()) > 0:
                        state.set_state('msg', 'Installing updates')
                        logger.info('Performing updates')
                        logger.info('Updates available:')
                        [logger.info('%s %s ->  %s' % (x, y['old'], y['new'])) for x, y in updates.items()]
                        try:
                            p.do_updates()
                        except subprocess.CalledProcessError:
                            state.set_state('inprogress', False)
                            state.set_state('prompt', True)
                            state.set_state('msg', 'Failed to install pacman updates, see logs for more detail')
                            logger.error('Failed to install updates')
                            logger.critical('{ENDWATCH}')
                            continue
                        did_something = True
                    state.set_state('update', False)

                if did_something:
                    state.set_state('msg', 'A reboot is required to complete updates')
                    state.set_state('rebootrequired', True)
                    state.set_state('prompt', True)
                else:
                    state.set_state('msg', 'No updates available')

                # Set status inactive
                state.set_state('inprogress', False)
                logger.info('Updates completed')
                logger.critical('{ENDWATCH}')

            time.sleep(15)
    except KeyboardInterrupt:
        logger.info('Exiting')
        Path('/tmp/.auc_secret').unlink(missing_ok=True)


def run():
    args = add_parser()

    log_format = '[AUC] [%(levelname)s] %(message)s'
    logging.basicConfig(level=log_levels[args.log_level],
                        handlers=[logging.StreamHandler(sys.stdout)],
                        format=log_format)
    logger = logging.getLogger(name="auc")

    run_daemon(args, logger)


if __name__ == '__main__':
    run()
