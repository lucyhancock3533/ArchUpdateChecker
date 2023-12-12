import subprocess
from datetime import datetime


class PacmanUpdater:
    def __init__(self, logger, log_path):
        self.logger = logger
        self.log_path = log_path

    def sync_db(self):
        self.logger.info('Syncronising pacman DB')
        try:
            paccmd = subprocess.run(['pacman', '-Sy'], check=True, capture_output=True, text=True)
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### pacman -Sy stdout #####')
                f.write(paccmd.stdout)
                f.write('##### pacman -Sy stderr #####')
                f.write(paccmd.stderr)
                f.write('\n')
        except subprocess.CalledProcessError as e:
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### pacman -Sy stderr #####')
                f.write(e.stderr)
                f.write('\n')
            raise e

    def get_updates(self):
        self.logger.info('Checking for updates in pacman DB')
        try:
            paccmd = subprocess.run(['pacman', '-Qnu'], check=True, capture_output=True, text=True)
            updates_list = paccmd.stdout.split('\n')
            split_updates = [x.split(' ') for x in updates_list if len(x) > 1]
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('Updates available:\n')
                f.write(paccmd.stdout)
                f.write('\n')
            return {x[0]: {'old': x[1], 'new': x[3]} for x in split_updates}
        except subprocess.CalledProcessError  as e:
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### pacman -Qnu stderr #####')
                f.write(e.stderr)
                f.write('\n')
            raise e

    def do_updates(self):
        self.logger.info('Installing updates with Pacman')
        try:
            paccmd = subprocess.run(['pacman', '-Su', '--noconfirm', '--noprogressbar'],
                                    check=True, capture_output=True, text=True)
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### pacman -Su --noconfirm --noprogressbar stdout #####')
                f.write(paccmd.stdout)
                f.write('##### pacman -Su --noconfirm --noprogressbar stderr #####')
                f.write(paccmd.stderr)
                f.write('\n')
        except subprocess.CalledProcessError as e:
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### pacman -Su --noconfirm --noprogressbar stderr #####')
                f.write(e.stderr)
                f.write('\n')
            raise e
