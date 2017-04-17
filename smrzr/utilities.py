from functools import wraps 
from collections import OrderedDict

def memoize(func):
    cache = LimitedSizeDict(size_limit=10)
    @wraps(func)
    def memoized(*args):
        try:
            return cache[args]
        except KeyError:
            result = cache[args] = func(*args)
            return result
    return memoized

class LimitedSizeDict(OrderedDict):
    '''stackoverflow.com/a/2437645/696668'''

    def __init__(self, *args, **kwds):

        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):

        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):

        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


