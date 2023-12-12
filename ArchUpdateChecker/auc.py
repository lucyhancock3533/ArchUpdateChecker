import logging
import sys

from argparse import ArgumentParser

from ArchUpdateChecker.daemon.daemon import add_subparser as daemon_subparse, run_daemon


def version(args, logger):
    logger.info('AUC v1.0.0-dev')


log_levels = {'error': logging.ERROR, 'warning': logging.WARNING, 'info': logging.INFO, 'debug': logging.DEBUG}
modes = {'version': version, 'daemon': run_daemon}


def run():
    parser = ArgumentParser()
    parser.add_argument('--log-level', type=str, default='info', nargs='?', choices=log_levels.keys())
    cmd_sub = parser.add_subparsers(dest='mode', required=True)
    cmd_sub.add_parser(name='version')
    daemon_sub = cmd_sub.add_parser(name='daemon')
    daemon_subparse(daemon_sub)
    args = parser.parse_args()

    log_format = '[AUC] [%(levelname)s] %(message)s'
    logging.basicConfig(level=log_levels[args.log_level],
                        handlers=[logging.StreamHandler(sys.stdout)],
                        format=log_format)
    logger = logging.getLogger(name="auc")

    modes[args.mode](args, logger)


if __name__ == "__main__":
    run()
