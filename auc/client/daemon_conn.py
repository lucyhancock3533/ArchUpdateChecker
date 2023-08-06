import requests


def get_status():
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/',  json={'function': 'status'})


def get_updates():
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'updates'})


def get_prompt():
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'prompt'})


def set_no_reboot(secret):
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'clear-reboot', 'secret': secret})


def set_update(secret):
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'update', 'secret': secret})


def set_run(secret):
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'run', 'secret': secret})


def connect_listener(secret, socket_path, socket_secret):
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={
                                                                    'function': 'connect',
                                                                    'secret': secret,
                                                                    'socket_path': socket_path,
                                                                    'socket_secret': socket_secret
    })
