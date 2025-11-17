import inspect
import json
import os
import shutil
import typing
import re
from enum import Enum
from threading import RLock

from common.jsonable import Jsonable

HOME_FOLDER = os.getcwd()
# DATE_TIME_STRING = "%Y-%m-%dT%H:%M:%S.%f"


def has_hours_minutes_seconds(timestamp: str):
    # Regular expression to match HH:MM:SS format
    if timestamp is None:
        return False
    pattern = r'\b\d{2}:\d{2}:\d{2}\b'
    match = re.search(pattern, timestamp)
    return bool(match)


class Singleton(type):
    _instances = {}
    singleton_lock = RLock()

    def __call__(cls, *args, **kwargs):
        cls.singleton_lock.acquire()
        try:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
        finally:
            cls.singleton_lock.release()


class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Jsonable):
            return obj.json
        elif isinstance(obj, Enum):
            return obj.value
        # Let the base class default method raise the TypeError
        return super(CustomJsonEncoder, self).default(obj)


class ConfigBase(metaclass=Singleton):
    """
     Container for configuration, loaded from JSON file
     """

    def __init__(self, filename: str):
        """
        Load the configuration from json or use the defaults
        :param filename: config file to use.
        """
        self.default_values_dict = self.json(include_empty_config=True)
        self.json_file = filename
        self.json_file_bak = filename + ".prev"
        if os.path.exists(self.json_file):
            try:
                self.reload()
            except ValueError:
                pass
        else:
            directory = os.path.dirname(self.json_file)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(self.json_file, "w") as fp:
                json.dump(self.json(), fp, indent=True)
            os.chmod(self.json_file, 0o644)

    def json(self, include_empty_config=False) -> typing.Dict:
        attributes = inspect.getmembers(self, lambda m: not (inspect.isroutine(m)))
        ret = {}
        for attr in attributes:
            if not (attr[0].startswith('__')) and ((attr[1] is not None) or include_empty_config):
                if isinstance(attr[1], Jsonable):
                    ret[attr[0]] = attr[1].json
                elif isinstance(attr[1], Enum):
                    ret[attr[0]] = attr[1].value
                else:
                    ret[attr[0]] = attr[1]
        # ret = {attr[0]: attr[1] for attr in attributes if not (attr[0].startswith('__')) and attr[1] is not None}
        return ret

    def update(self, conf: typing.Dict = None, persist: bool = False, only_field: str = None):
        valid_atr = [z for z in dir(self) if not self.__bad_key(z)]
        if conf is not None:
            for (k, v) in list(conf.items()):
                if k in valid_atr:
                    setattr(self, k, v)

        if os.path.exists(self.json_file):
            shutil.copyfile(self.json_file, self.json_file_bak)

        if persist:
            if only_field is None:
                with open(self.json_file, "w") as fp:
                    json.dump(self.json(), fp, cls=CustomJsonEncoder, indent=True)
                os.chmod(self.json_file, 0o644)
            else:
                value_to_update = self.json()[only_field]
                _conf = json.load(open(self.json_file, "r"))
                _conf[only_field] = value_to_update
                with open(self.json_file, "w") as fp:
                    json.dump(_conf, fp, cls=CustomJsonEncoder, indent=True)
                os.chmod(self.json_file, 0o644)

    def reload(self):
        conf = json.load(open(self.json_file, "r"))
        self.__dict__.update(conf)

    def __bad_key(self, prop):
        attr = getattr(type(self), prop, None)
        private = '_' + self.__class__.__name__ in prop
        return private or prop.startswith("_") or isinstance(attr, property) or inspect.isroutine(attr)
