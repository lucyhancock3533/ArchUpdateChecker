import logging
import sys

from argparse import ArgumentParser


def run():
    log_format = '[AUC] [%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)], format=log_format)
    logger = logging.getLogger(name="auc")

    parser = ArgumentParser()
    parser.add_argument('mode', type=str)
    args = parser.parse_args()

    if args.mode not in modes:
        logger.error('Invalid mode (%s) specified' % args.mode)
    else:
        modes[args.mode](args, logger)


def version(args, logger):
    logger.info('AUC v1.0.0-dev')


modes = {'version': version}

if __name__ == "__main__":
    run()
