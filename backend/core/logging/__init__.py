

class BaseLogger:
    def __init__(self, log_level: str, log_dir: str):
        self.log_level = log_level
        self.log_dir = log_dir
