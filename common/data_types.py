import typing
from enum import Enum

from common.jsonable import Jsonable


class DataLoadType(Enum):
    DataBaseQuery = 1
    Local = 2
    API = 3


class DataSourcePointer(Jsonable):
    ip = ''
    usr = ''
    password = ''

    def __int__(self, json_dict: typing.Dict = {}):
        super(DataSourcePointer, self).__init__(json_dict)
