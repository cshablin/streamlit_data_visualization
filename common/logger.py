import logging
from abc import ABC, abstractmethod

from common.config import Config
from common.init_app import log_name


class LoggerBase(ABC):

    @abstractmethod
    def __init__(self, name: str, conf: Config):
        self._logger = logging.getLogger(name)
        self.name = self._logger.name
        self.config = conf
        self._logger.setLevel(level=conf.NUM_LOG_FILES)

    def fatal(self, msg, *args):
        self._logger.fatal(msg.format(*args))
        if self.config.PRINT_TO_CONSOLE:
            print(msg.format(*args))

    def info(self, msg, *args):
        self._logger.info(msg.format(*args))
        if self.config.PRINT_TO_CONSOLE:
            print(msg.format(*args))

    def error(self, msg, *args):
        self._logger.error(msg.format(*args))
        if self.config.PRINT_TO_CONSOLE:
            print(msg.format(*args))

    def warn(self, msg, *args):
        self._logger.warning(msg.format(*args))
        if self.config.PRINT_TO_CONSOLE:
            print(msg.format(*args))

    def debug(self, msg, *args):
        self._logger.debug(msg.format(*args))
        if self.config.PRINT_TO_CONSOLE:
            print(msg.format(*args))

    def flush(self):
        self.info("flushing logs")
        [h.flush() for h in self._logger.handlers]
        self.info("done flushing logs")


class Logger(LoggerBase):
    def __init__(self, name: str = log_name, conf: Config = Config()):
        super(Logger, self).__init__(name, conf)

    # def __int__(self, name=log_name):
    #     conf = Config()
    #     super(Logger, self).__init__(name, conf)
