import json
import importlib
import itertools

class StopServer(Exception):
    """Raise to stop the server."""

class Server:

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.objs = {}

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
        logfr(line, end='')
        return line

    def send(self, response):
        logfr(response)
        self.outfile.write(response + '\n')
        self.outfile.flush()

    def handle_json(self, json_line):
        try:
            request = json.loads(json_line)
        except ValueError:
            return json.dumps({"error": "could not parse json"})
        response = self.handle(request)
        return json.dumps(response)

    def handle(self, request):
        if 'module' in request:
            try:
                module = importlib.import_module(request['module'])
            except Exception as err:
                return self.makeerror('exception during import: {}'.format(err))
            return self.makeresult(module)

        if 'oid' in request:
            oid = request['oid']
            try:
                obj = self.objs[oid]
            except KeyError:
                return self.makeerror('object does not exist')

        if 'method' in request:
            if 'params' in request:
                try:
                    params = map(self.deref, request['params'])
                except TypeError:
                    return self.makeerror('params should be a list')
            else:
                params = []
            try:
                method_name = request['method']
                method = getattr(obj, method_name)
            except AttributeError as e:
                return self.makeerror('method "{}" does not exist'.format(method_name))
            if not callable(method):
                return self.makeerror('method "{}" does not exist'.format(method_name))

            try:
                result = method(*params)
            except Exception as err:
                return self.makeerror('exception during call: {}'.format(err))

            return self.makeresult(result)

        if 'attr' in request:
            try:
                attr = getattr(obj, request['attr'])
            except AttributeError:
                return self.makeerror('attr does not exist')
            return self.makeresult(attr)

        return self.makeerror('no request specified')

    def makeresult(self, result):
        return {'result': self.getref(result)}

    def makeerror(self, error):
        return {'error': error}

    def getref(self, obj):
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, list):
            return list(map(self.getref, obj))
        elif isinstance(obj, dict):
            return {self.getref(key): self.getref(val)
                    for key, val in obj.items()}

        oid = id(obj)
        if oid not in self.objs:
            self.objs[oid] = obj
        return {'__oid__': oid}

    def deref(self, obj):
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, list):
            return list(map(self.deref, obj))
        elif isinstance(obj, dict):
            if '__oid__' in obj:
                oid = obj['__oid__']
                return self.objs[oid]
            return {self.deref(key): self.deref(val)
                    for key, val in obj.items()}
        raise RuntimeError('cannot deref unexpected object: {}'.format(obj))

    def next_id(self):
        return next(self._idgen)

def logfr(*args, **kwargs):
    with open('/tmp/logfr', 'a') as tmplog:
        print(*args, file=tmplog, **kwargs)
