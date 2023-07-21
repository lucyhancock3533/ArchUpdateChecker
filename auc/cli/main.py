from multiprocessing.connection import Client


def get_status(client, logger):
    client.send('status')
    logger.info(client.recv())


def clear_reboot(client, logger):
    client.send('clear-reboot')
    logger.info(client.recv())


def get_updates(client, logger):
    client.send('updates')
    update_dict = client.recv()
    for k, v in update_dict.items():
        logger.info('%s from %s to %s' % (k, v['old'], v['new']))


def add_subparser(subparser):
    subparser.add_argument('clicmd', type=str, choices=cmds.keys())


def run_cli(args, logger):
    with open('/tmp/.auc_secret', 'r') as f:
        secret = f.read()
    client = Client('/tmp/.auc_socket', family='AF_UNIX', authkey=secret.encode())
    cmds[args.clicmd](client, logger)
    client.close()


cmds = {'status': get_status, 'updates': get_updates, 'clear-reboot':  clear_reboot}
