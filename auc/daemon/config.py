import yaml


class AucConfig:
    def __init__(self, config_path, logger):
        try:
            with open(config_path, 'r') as f:
                config_file = f.read()
                config = yaml.safe_load(config_file)
        except FileNotFoundError:
            logger.warning('Config file not found, using defaults')
            config = {}
        self._mr_url = config.get('mr_url', 'https://archlinux.org/mirrorlist/?country=all&protocol=http&protocol=https'
                                       '&ip_version=4&ip_version=6&use_mirror_status=on')
        self._update_mr = config.get('update_mr', False)
        self._log_path = config.get('log_path', '/var/log/auc')

    @property
    def mr_url(self):
        return self._mr_url

    @property
    def update_mr(self):
        return self._update_mr

    @property
    def log_path(self):
        return self._log_path
