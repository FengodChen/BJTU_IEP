import logging

LOGING_LEVEL = logging.INFO

class Log:
    def __init__(self, file_path:str):
        self.logger = logging.getLogger()
        self.logger.setLevel(LOGING_LEVEL)
        fh = logging.FileHandler(file_path, mode='a')
        fh.setLevel(LOGING_LEVEL)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    
    def debug(self, inf:str):
        self.logger.debug(inf)
    
    def info(self, inf:str):
        self.logger.info(inf)
    
    def warning(self, inf:str):
        self.logger.warning(inf)
    
    def error(self, inf:str):
        self.logger.error(inf)
    
    def critical(self, inf:str):
        self.logger.critical(inf)