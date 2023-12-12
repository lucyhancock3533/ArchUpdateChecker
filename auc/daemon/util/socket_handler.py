import json
import struct
from logging import LogRecord
from logging.handlers import SocketHandler


class JsonSocketHandler(SocketHandler):
    def makePickle(self, record: LogRecord) -> bytes:
        # Derived from SockerHandler makePickle replacing pickle with json
        ei = record.exc_info
        if ei:
            # just to get traceback text into record.exc_text
            dummy = self.format(record)
        d = dict(record.__dict__)
        d['msg'] = record.getMessage()
        d['args'] = None
        d['exc_info'] = None
        d.pop('message', None)
        s = json.dumps(d).encode()
        slen = struct.pack(">L", len(s))
        return slen + s
