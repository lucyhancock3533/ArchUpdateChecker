import subprocess
from datetime import datetime


class YayUpdater:
    def __init__(self, logger, log_path):
        self.logger = logger
        self.log_path = log_path

    def sync_db(self):
        self.logger.info('Syncronising pacman DB')
        try:
            paccmd = subprocess.run(['yay', '-Sy'], check=True, capture_output=True, text=True)
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### yay -Sy stdout #####')
                f.write(paccmd.stdout)
                f.write('##### yay -Sy stderr #####')
                f.write(paccmd.stderr)
                f.write('\n')
        except subprocess.CalledProcessError as e:
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### yay -Sy stderr #####')
                f.write(e.stderr)
                f.write('\n')
            raise e

    def get_updates(self):
        self.logger.info('Checking for updates in pacman DB')
        try:
            paccmd = subprocess.run(['yay', '-Qu'], check=True, capture_output=True, text=True)
            updates_list = paccmd.stdout.split('\n')
            split_updates = [x.split(' ') for x in updates_list if len(x) > 1]
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('Updates available:\n')
                f.write(paccmd.stdout)
                f.write('\n')
            return {x[0]: {'old': x[1], 'new': x[3]} for x in split_updates}
        except subprocess.CalledProcessError  as e:
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### yay -Qu stderr #####')
                f.write(e.stderr)
                f.write('\n')
            raise e

    def do_updates(self):
        self.logger.info('Installing updates with Pacman')
        try:
            paccmd = subprocess.run(['yay', '-Su', '--noconfirm', '--noprogressbar'],
                                    check=True, capture_output=True, text=True)
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### yay -Su --noconfirm --noprogressbar stdout #####')
                f.write(paccmd.stdout)
                f.write('##### yay -Su --noconfirm --noprogressbar stderr #####')
                f.write(paccmd.stderr)
                f.write('\n')
        except subprocess.CalledProcessError as e:
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log', 'a') as f:
                f.write('##### yay -Su --noconfirm --noprogressbar stderr #####')
                f.write(e.stderr)
                f.write('\n')
            raise e
