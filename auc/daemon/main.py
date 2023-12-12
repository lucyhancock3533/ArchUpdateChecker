from auc.daemon.listener import DaemonListener


def add_subparser(subparser):
    pass


def run_daemon(args, logger):
    l = DaemonListener(args, logger)
    l.listen_loop()
