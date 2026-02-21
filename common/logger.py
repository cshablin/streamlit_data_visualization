import logging

from common.config import Config
from common.init_app import log_name


class LoggerBase:

    def __init__(self, name: str, conf: Config):
        self._logger = logging.getLogger(name)
        self.name = self._logger.name
        self.config = conf
        self._logger.setLevel(level=conf.LOGGING_LEVEL)

    def fatal(self, msg, *args):
        formatted = msg.format(*args)
        self._logger.fatal(formatted)
        if self.config.PRINT_TO_CONSOLE:
            print(formatted)

    def info(self, msg, *args):
        formatted = msg.format(*args)
        self._logger.info(formatted)
        if self.config.PRINT_TO_CONSOLE:
            print(formatted)

    def error(self, msg, *args):
        formatted = msg.format(*args)
        self._logger.error(formatted)
        if self.config.PRINT_TO_CONSOLE:
            print(formatted)

    def warn(self, msg, *args):
        formatted = msg.format(*args)
        self._logger.warning(formatted)
        if self.config.PRINT_TO_CONSOLE:
            print(formatted)

    def debug(self, msg, *args):
        formatted = msg.format(*args)
        self._logger.debug(formatted)
        if self.config.PRINT_TO_CONSOLE:
            print(formatted)

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
