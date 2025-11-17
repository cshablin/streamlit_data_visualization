import inspect


class Jsonable(object):

    def __init__(self, _json):
        self.json = _json  # this will actually call the setter

    def __bad_key(self, prop):
        attr = getattr(type(self), prop, None)
        private = '_' + self.__class__.__name__ in prop
        return private or prop.startswith("_") or isinstance(attr, property) or inspect.isroutine(attr)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Jsonable):
            return self.json == other.json
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def json(self):
        ret = {}

        for key in [z for z in dir(self) if not self.__bad_key(z)]:
            ret[key] = getattr(self, key)
        return ret

    @json.setter
    def json(self, value):
        if value:
            for k, v in list(value.items()):
                if hasattr(self, k):
                    setattr(self, k, v)
                else:
                    found = False
                    for cur_k in [z for z in dir(self) if not self.__bad_key(z)]:
                        if k.lower() == cur_k.lower():
                            setattr(self, cur_k, v)
                            found = True
                            break
                    if not found:
                        setattr(self, k, v)
