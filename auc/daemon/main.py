import subprocess
import time

from threading import Thread
from pathlib import Path
from pythonping import ping

from auc.daemon.listener import DaemonListener
from auc.daemon.config import AucConfig
from auc.daemon.state import AucState
from auc.daemon.mirrorlist import MirrorlistUpdate
from auc.daemon.pacman_updater import PacmanUpdater


def add_subparser(subparser):
    subparser.add_argument('--config', type=str, default='/etc/auc.yaml', nargs='?')


def check_network(ping_addr, logger):
    logger.debug('Pinging %s', ping_addr)
    res = ping(target=ping_addr, count=1)
    while not res.success():
        time.sleep(60)
        logger.debug('Pinging %s', ping_addr)
        res = ping(target=ping_addr, count=1)


def run_daemon(args, logger):
    logger.info('Starting AUC daemon')
    config = AucConfig(args.config, logger)
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
                network = False
                state.set_state('msg', 'Waiting for network connection')
                logger.info('Checking for network connection')
                while not network:
                    try:
                        check_network(config.ping_addr, logger)
                        network = True
                    except OSError:
                        logger.debug('No network connection')
                        time.sleep(60)

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
                        continue

                # Do updates
                if state.access_state('update'):
                    p = PacmanUpdater(logger, config.log_path)
                    logger.info('Updating pacman database')
                    try:
                        p.sync_db()
                    except subprocess.CalledProcessError:
                        logger.error('Failed to check for updates')
                        state.set_state('inprogress', False)
                        state.set_state('prompt', True)
                        state.set_state('msg', 'Failed to sync pacman DB, see logs for more detail')
                        continue

                    try:
                        updates = p.get_updates()
                        state.set_state('updates', updates)
                    except subprocess.CalledProcessError:
                        logger.info('No updates are available')
                        updates = {}

                    if len(updates.keys()) > 0:
                        logger.info('Performing updates')
                        logger.info('Updates available:')
                        [logger.info('%s %s ->  %s' % (x, y['old'], y['new'])) for x, y in updates.items()]
                        try:
                            p.do_updates()
                        except subprocess.CalledProcessError:
                            state.set_state('inprogress', False)
                            state.set_state('prompt', True)
                            state.set_state('msg', 'Failed to install pacman updates, see logs for more detail')
                            continue
                        did_something = True
                    state.set_state('update', False)

                if did_something:
                    state.set_state('msg', 'A reboot is required to complete updates')
                    state.set_state('rebootrequired', True)
                    state.set_state('prompt', True)
                else:
                    state.set_state('msg', 'Nothing to do')

                # Set status inactive
                state.set_state('inprogress', False)
                logger.info('Updates completed')

            time.sleep(300)
    except KeyboardInterrupt:
        logger.info('Exiting')
        Path('/tmp/.auc_secret').unlink(missing_ok=True)
