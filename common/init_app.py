import os
import logging.handlers

from common.config import Config

log_name = 'temporal_analysis'
log = logging.getLogger(log_name)
log.setLevel(logging.DEBUG)
LOG_FOLDER = 'log'
MY_LOG = LOG_FOLDER + os.path.sep + "temporal_analysis.log"
_log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
conf = Config()
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

SERVER_LOG_BACKUP_COUNT = 10

handler = logging.handlers.RotatingFileHandler(
    MY_LOG, maxBytes=5 * 1024 * 1024, backupCount=conf.NUM_LOG_FILES)
formatter = logging.Formatter(_log_format)
handler.setFormatter(formatter)
log.addHandler(handler)
