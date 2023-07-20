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
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log') as f:
                f.write(paccmd.stdout)
                f.write(paccmd.stderr)
        except subprocess.CalledProcessError as e:
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log') as f:
                f.write(e.stderr)
            raise e

    def get_updates(self):
        self.logger.info('Checking for updates in pacman DB')
        try:
            paccmd = subprocess.run(['pacman', '-Qnu'], check=True, capture_output=True, text=True)
            updates_list = paccmd.stdout.split('\n')
            split_updates = [x.split(' ') for x in updates_list if len(x) > 1]
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log') as f:
                f.write('\nUpdates available:\n')
                f.write(paccmd.stdout)
            return {x[0]: {'old': x[1], 'new': x[3]} for x in split_updates}
        except subprocess.CalledProcessError  as e:
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log') as f:
                f.write(e.stderr)
            raise e

    def do_updates(self):
        self.logger.info('Installing updates with Pacman')
        try:
            paccmd = subprocess.run(['pacman', '-Su'], check=True, capture_output=True, text=True)
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log') as f:
                f.write(paccmd.stdout)
                f.write(paccmd.stderr)
        except subprocess.CalledProcessError as e:
            with open(f'{self.log_path}/auc_pacman_{datetime.today().strftime("%Y-%m-%d")}.log') as f:
                f.write(e.stderr)
            raise e
