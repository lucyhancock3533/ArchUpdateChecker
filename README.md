# ArchUpdateChecker

A daemonized Arch Linux automatic updater.

Requirements:
* pacman
* Python 3.11+
* Dependencies are managed by poetry for dev

Usage:
* Start daemon `aucd`
  * `--config` Overrise config file location (Usually /etc/auc.yaml)
* Interactive cli `auc <command>`
  * Commands
    * `status` Gets current status of updater
    * `updates` Get updates performed
    * `clear-reboot` Clear reboot if unneeded

Config file example:
```
---
update_mr: True (Defaut False)
mr_url: '<URL to live mirrorlist>' (Default https://archlinux.org/mirrorlist/?country=all&protocol=http&protocol=https&ip_version=4&ip_version=6&use_mirror_status=on)
log_path: '<path to store file logs>' (Default /var/log/auc)
file_log: True (Default True)
ping_addr: '<Address to ping in order to check for network connection>' (Default 1.1.1.1)
```