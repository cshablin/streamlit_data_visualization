import inspect
import json
import os
import platform
import shutil


# HOME_FOLDER = 'c:\\feed_watcher' #  if platform.system() == 'Windows' else '/path/to/folder'
from threading import Lock

HOME_FOLDER = os.getcwd()
DATE_TIME_STRING = "%Y-%m-%dT%H:%M:%S.%f"


class Singleton(type):
    _instances = {}
    singleton_lock = Lock()

    def __call__(cls, *args, **kwargs):
        cls.singleton_lock.acquire()
        try:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
        finally:
            cls.singleton_lock.release()


class Config(metaclass=Singleton):
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

    def __init__(self, filename: str = HOME_FOLDER + os.path.sep + "data_analysis.json"):
        """
        Load the configuration from json or use the defaults
        :param filename: config file to use.
        """
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

    def json(self):
        attributes = inspect.getmembers(self, lambda m: not (inspect.isroutine(m)))
        ret = {}
        for attr in attributes:
            if not (attr[0].startswith('__')) and attr[1] is not None:
                ret[attr[0]] = attr[1]
        # ret = {attr[0]: attr[1] for attr in attributes if not (attr[0].startswith('__')) and attr[1] is not None}
        return ret

    def update(self, conf=None):
        if conf is not None:
            for (k, v) in list(conf.items()):
                setattr(self, k, v)

        if os.path.exists(self.json_file):
            shutil.copyfile(self.json_file, self.json_file_bak)

        with open(self.json_file, "w") as fp:
            json.dump(self.json(), fp, indent=True)
        os.chmod(self.json_file, 0o644)

        self.reload()

    def reload(self):
        conf = json.load(open(self.json_file, "r"))
        self.__dict__.update(conf)
