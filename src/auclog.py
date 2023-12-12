#! /usr/bin/python3
"""AUC logging module for GUI/CLI logging"""

class Logger():
	def __init__(self):
		log_folder = Path(os.path.expanduser("~/.auc/"))
		log_folder.mkdir(parents=True, exist_ok=True) # Ensure folder exists
		self.log_file = open(os.path.expanduser("~/.auc/") + str(datetime.now()) + ".log", "w")
	
	def log_write(self, text):
		lead_str = "[(AUC) " + str(datetime.now()) + "] "
		self.log_file.write(lead_str + text)
	def log_close(self):
		self.log_file.close()