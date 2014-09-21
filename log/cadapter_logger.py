
import os
import logging
import logging.config

LOG_CONFIG_FILE = os.getcwd()+"\\log\\logger.conf" 

class CAdapterLogger():
    def __init__(self, logtype = "", confFile = LOG_CONFIG_FILE):
        logging.config.fileConfig(confFile)
        self.logger = logging.getLogger(logtype)
        
    def debug(self,msg = "debug"):
        self.logger.debug(msg)
    
    def info(self, msg = "info"):
        self.logger.info(msg)
    
    def warn(self, msg = "warn"):
        self.logger.warning(msg)
        
    def error(self, msg = "error"):
        self.logger.error(msg) 
    
    def critical(self, msg = "critical"):
        self.logger.critical(msg)

# if __name__ == "__main__":
#     logger = CAdapterLogger()
#     for i in range(10000):
#         logger.info("program is starting")
#         logger.debug("no debug")
#         logger.warn("no warning")
#         logger.info("program is ending......")
    
    
    

    

            
    