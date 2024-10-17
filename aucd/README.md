# ArchUpdateChecker

A daemonized Arch Linux automatic updater.

### Requirements
* pacman
* Python 3.11+
* For GTK prompter:
  * GTK 4
  * libadwaita
  * cairo
  * gobject-introspection

### Usage
* Start daemon `aucd`
  * `--config` Override config file location (Usually /etc/auc.yaml)
* Interactive cli `auc <command>`
  * Commands
    * `status` Gets current status of updater
    * `updates` Get updates performed
    * `clear-reboot` Clear reboot if unneeded
* Start GTK prompt `aucp` 

### Use with yay
Using with yay to update both system and auc packages is possible but requires extra configuration and security consideration. To use with yay `aucd` must be ran as a non-root user that has passwordless sudo permissions to run the pacman command. There is also some inherent risk as yay will be used to update AUR package with no confirmation or prompting og the PKGBUILD, it's perfectly possible for a malicious actor to insert exploits into AUR packages installed unattended. I take no responsibility for any loss or damage caused.

### Config file example
```
---
update_mr: True (Defaut False)
mr_url: '<URL to live mirrorlist>' (Default https://archlinux.org/mirrorlist/?country=all&protocol=http&protocol=https&ip_version=4&ip_version=6&use_mirror_status=on)
log_path: '<path to store file logs>' (Default /var/log/auc)
file_log: True (Default True)
use_yay: False (Defaut False)
ping_addr: '<URL to check network connectivity>' (Default https://1.1.1.1)
```
