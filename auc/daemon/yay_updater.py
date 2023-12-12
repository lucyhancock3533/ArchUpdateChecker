import subprocess

from auc.daemon.util.logger_io import LoggerIO


class YayUpdater:
    def __init__(self, logger, log_path):
        self.logger = logger
        self.log_path = log_path

    def sync_db(self):
        self.logger.info('Syncronising pacman DB')
        paccmd = subprocess.Popen(['yay', '-Sy'], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log_out = LoggerIO(self.logger, 'yay')
        for i in iter(lambda: paccmd.stdout.read(1), ""):
            log_out.write(i)
        paccmd.wait()
        log_out.finish()
        if paccmd.returncode != 0:
            raise subprocess.CalledProcessError(paccmd.returncode, paccmd.args)

    def get_updates(self):
        self.logger.info('Checking for updates in pacman DB')
        try:
            paccmd = subprocess.run(['yay', '-Qyu'], check=True, capture_output=True, text=True)
            updates_list = paccmd.stdout.split('\n')
            split_updates = [x.split(' ') for x in updates_list if len(x) > 1]
            return {x[0]: {'old': x[1], 'new': x[3]} for x in split_updates}
        except subprocess.CalledProcessError as e:
            raise e

    def do_updates(self):
        self.logger.info('Installing updates with Pacman')
        paccmd = subprocess.Popen(['yay', '-Su', '--noconfirm', '--noprogressbar'],
                                  text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log_out = LoggerIO(self.logger, 'yay')
        for i in iter(lambda: paccmd.stdout.read(1), ""):
            log_out.write(i)
        paccmd.wait()
        log_out.finish()
        if paccmd.returncode != 0:
            raise subprocess.CalledProcessError(paccmd.returncode, paccmd.args)
