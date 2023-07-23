import socketserver


class UnixHTTPServer(socketserver.UnixStreamServer):
    def __init__(self, server_address, handler, state, logger, secret):
        super().__init__(server_address, handler)
        self.logger = logger
        self.state = state
        self.secret = secret

    def get_request(self):
        request, client_address = super(UnixHTTPServer, self).get_request()
        return request, ["local", 0]
