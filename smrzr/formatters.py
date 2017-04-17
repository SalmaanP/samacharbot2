class Formatter:

    def __init__(self, key_points,fmt):

        if not hasattr(self, fmt):
            raise ValueError("invalid option: use 'md', 'json' or 'html'")

        self._fmt = fmt
        self._kp = key_points
        self._options = {
                         'default': self.default,
                         'md'  : self.md,
                         'json': self.json,
                         'html':self.html,
                        }

    def frmt(self):
        return self._options[self._fmt]()

    def default(self):
        return self._kp

    def md(self):
        fs = u""
        for i in xrange(len(self._kp)):
            fs += ">* {{{}}}\n".format(i)
        return fs.format(*self._kp)

    def json(self):
        raise NotImplementedError

    def html(self):
        raise NotImplementedError
