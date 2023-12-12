from auc.daemon.listener import DaemonListener
from auc.daemon.config import AucConfig


def add_subparser(subparser):
    subparser.add_argument('--config', type=str, default='/etc/auc.yaml', nargs='?')


def run_daemon(args, logger):
    logger.info('Starting AUC daemon')
    config = AucConfig(args.config, logger)
