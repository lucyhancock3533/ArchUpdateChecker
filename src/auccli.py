from aucpacman import sync_db, get_update_count, get_ignore_count, get_updates, run_updates
from aucpmml import get_mrl_url, set_mrl_url, update_mrl
"""Module dealing with cli for AUC"""

def run_auc_cli():
    print("ArchUpdateChecker v0-git")
    mirrorlist = get_mrl_url()
    if(mirrorlist == ""):
        pass
    elif(mirrorlist == "NOMRLUPD"):
        run_auc()
    else:
        update_mrl()
        run_auc()

def run_auc():
    sync_db()
    if (get_update_count() > 0):
        prompt_updates()
    else:
        print("No updates are available")

def prompt_updates():
    pass

def do_updates():
    pass
