class LoggerIO:
    def __init__(self, logger, prefix=''):
        self.buffer = []
        self.logger = logger
        self.prefix = prefix

    def write(self, c):
        if c == '\n':
            self._write_line()
        else:
            self.buffer.append(c)

    def write_full(self, i):
        lines = i.split('\n')
        for line in lines:
            self.logger.info('<%s> %s' % (self.prefix, line))

    def finish(self):
        if self.buffer:
            self._write_line()

    def _write_line(self):
        line = ''.join(self.buffer)
        self.logger.info('<%s> %s' % (self.prefix, line))
        self.buffer = []
