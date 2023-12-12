import requests


class MirrorlistUpdate:
    def __init__(self, mr_url, logger):
        self.mr_url = mr_url
        self.logger = logger

    def update_mirrorlist(self):
        self.logger.info('Updating pacman mirror list from %s' % self.mr_url)
        mrl = requests.get(self.mr_url)
        if mrl.status_code != requests.codes.ok:
            self.logger.error('Failed to fetch new mirror list')
            return False
        with open('/etc/pacman.d/mirrorlist', 'w') as f:
            f.write(mrl.text.replace('#S', 'S'))
        self.logger.info('Pacman mirror list updated')
        return True
