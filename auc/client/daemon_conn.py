import requests


def get_status():
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/',  json={'function': 'status'})


def get_updates():
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'updates'})


def get_prompt():
    return requests.post('http+unix://%2Ftmp%2F.auc_socket/', json={'function': 'prompt'})
