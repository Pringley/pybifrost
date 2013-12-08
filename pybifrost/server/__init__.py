import json

class Server:

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def start(self):
        while True:
            line = self.infile.readline()
            if not line:
                break # stop at EOF
            try:
                request = json.loads(line)
            except ValueError:
                self.send({"error": "could not parse json"})
                continue
            response = {} # dummy response
            self.send(response)

    def send(self, message):
        self.outfile.write(json.dumps(message, self.outfile) + '\n')
        self.outfile.flush()
