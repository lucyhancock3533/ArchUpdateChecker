import time

from threading import Thread

from auc.daemon.listener import DaemonListener
from auc.daemon.config import AucConfig
from auc.daemon.state import AucState
from auc.daemon.mirrorlist import MirrorlistUpdate


def add_subparser(subparser):
    subparser.add_argument('--config', type=str, default='/etc/auc.yaml', nargs='?')


def run_daemon(args, logger):
    logger.info('Starting AUC daemon')
    config = AucConfig(args.config, logger)
    state = AucState()

    # Start listener thread
    logger.info('Starting listener')
    listener = DaemonListener(args, logger, state)
    lt = Thread(target=listener.listen_loop)
    lt.start()

    try:
        while True:
            if state.access_state('inprogress'):
                logger.info('Executing updates')

                # Update mirrorlist
                if config.update_mr and state.access_state('mirrorlist'):
                    mrl = MirrorlistUpdate(config.mr_url, logger)
                    mrl.update_mirrorlist()
                    state.set_state('mirrorlist', False)

                # Do updates
                if state.access_state('update'):
                    state.set_state('update', False)

                # Set status inactive
                state.set_state('inprogress', False)

                if state.access_state('rebootrequired'):
                    state.set_state('msg', 'A reboot is required to complete updates')
                else:
                    state.set_state('msg', 'Updates completed')

                state.set_state('prompt', True)
                logger.info('Updates completed')

            time.sleep(300)
    except KeyboardInterrupt:
        logger.info('Exiting')

