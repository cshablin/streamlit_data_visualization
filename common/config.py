import os
import typing

from common.config_base import ConfigBase
from common.data_types import DataLoadType, DataSourcePointer

HOME_FOLDER = os.getcwd()
DATE_TIME_STRING = "%Y-%m-%dT%H:%M:%S.%f"


class Config(ConfigBase):
    """
    Container for configuration, loaded from JSON
    """

    PRINT_TO_CONSOLE = False
    NUM_LOG_FILES = 10
    LOGGING_LEVEL = 20
    # DEBUG = 10
    # INFO = 20
    # WARNING = 30
    # ERROR = 40
    # CRITICAL = 50

    # DB related
    DATA_LOADING_METHOD = DataLoadType.Local
    DATA_SOURCE_POINTER = DataSourcePointer(
        {
            "ip": "",
            "user": "",
            "password": ""
        }
    )

    def __init__(self, filename: str = HOME_FOLDER + os.path.sep + "data_analysis.json"):
        super().__init__(filename)
        self.__construct_special_types()

    def update(self, conf: typing.Dict = None, persist: bool = False, only_field: str = None):
        super().update(conf, persist)
        self.__construct_special_types()

    def reload(self):
        super().reload()
        self.__construct_special_types()

    def __construct_special_types(self):
        if isinstance(self.DATA_SOURCE_POINTER, typing.Dict):
            self.DATA_SOURCE_POINTER = DataSourcePointer(self.DATA_SOURCE_POINTER)
        self.DATA_LOADING_METHOD = DataLoadType(self.DATA_LOADING_METHOD)
