import logging
from os.path import join as pathJoin

from aw.timestamper import TimeStamper
from conf import ROOT_DIR, LOG_ER_FILE, LOG_STD_FILE

class Logger:
    def __init__(self, timestamper: TimeStamper) -> None:
        self.errorLogger = logging.getLogger("Error logger")
        self.standardLogger = logging.getLogger("Standard logger")
        
        self.erFileHandler = logging.FileHandler(pathJoin(ROOT_DIR, LOG_ER_FILE))
        self.stdFileHandler = logging.FileHandler(pathJoin(ROOT_DIR, LOG_STD_FILE))

    def logError(self, msg: str) -> None:
        formattedMsg = f"{self.timestamper.getDateTimeStamp()} ::: {msg}"
        self.errorLogger(formattedMsg)
    
    def logStandard(self, msg: str) -> None:
        formattedMsg = f"{self.timestamper.getDateTimeStamp()} ::: {msg}"
        self.standardLogger(formattedMsg)

