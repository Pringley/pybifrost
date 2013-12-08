import json

class StopServer(Exception):
    """Raise to stop the server."""

class Server:

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def start(self):
        try:
            while True:
                request = self.recv()
                response = self.handle_json(request)
                self.send(response)
        except StopServer:
            pass

    def recv(self):
        line = self.infile.readline()
        if not line:
            raise StopServer # stop at EOF
        return line

    def send(self, response):
        self.outfile.write(response + '\n')
        self.outfile.flush()

    def handle_json(self, json_line):
        try:
            request = json.loads(json_line)
        except ValueError:
            return json.dumps({"error": "could not parse json"})
        response = self._handle(request)
        return json.dumps(response)

    def _handle(self, request):
        return {}
