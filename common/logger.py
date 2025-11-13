import logging

from common.init_app import log_name


class Logger:

    def __init__(self, name=log_name):
        self._logger = logging.getLogger(name)
        self.name = self._logger.name

    def fatal(self, msg, *args):
        self._logger.fatal(msg.format(*args))

    def info(self, msg, *args):
        self._logger.info(msg.format(*args))

    def error(self, msg, *args):
        self._logger.error(msg.format(*args))

    def warn(self, msg, *args):
        self._logger.warning(msg.format(*args))

    def debug(self, msg, *args):
        self._logger.debug(msg.format(*args))

    def flush(self):
        self.info("flushing logs")
        [h.flush() for h in self._logger.handlers]
        self.info("done flushing logs")