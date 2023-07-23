import requests
import requests_unixsocket


def get_status(client, logger):
    r = requests.post('http+unix://%2Ftmp%2F.auc_socket/',  json={'function': 'status'})
    if r.status_code == 200:
        logger.info(r.json()['status'])
    elif 'error' in r.json():
        logger.error(r.json()['error'])
    else:
        logger.error('Unknown error')


def clear_reboot(client, logger):
    r = requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'clear-reboot'})
    if r.status_code == 200:
        logger.info(r.json()['msg'])
    elif 'error' in r.json():
        logger.error(r.json()['error'])
    else:
        logger.error('Unknown error')


def get_updates(client, logger):
    r = requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'clear-reboot'})
    if r.status_code == 200:
        for k, v in r.json()['updates'].items():
            logger.info('%s from %s to %s' % (k, v['old'], v['new']))
    elif 'error' in r.json():
        logger.error(r.json()['error'])
    else:
        logger.error('Unknown error')


def add_subparser(subparser):
    subparser.add_argument('clicmd', type=str, choices=cmds.keys())


def run_cli(args, logger):
    requests_unixsocket.monkeypatch()
    cmds[args.clicmd](logger)


cmds = {'status': get_status, 'updates': get_updates, 'clear-reboot':  clear_reboot}
