from multiprocessing.connection import Client


def add_subparser(subparser):
    pass


def run_cli(args, logger):
    with open('/tmp/.auc_secret', 'r') as f:
        secret = f.read()
    client = Client('/tmp/.auc_socket', family='AF_UNIX', authkey=secret.encode())
    client.send('test')
    print(client.recv())
    client.close()
