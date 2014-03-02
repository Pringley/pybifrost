import json
import subprocess
import collections.abc

from pybifrost.proxy import Proxy

def python():
    return PyBifrost('python3 -mpybifrost.server')

class PyBifrost:

    def __init__(self, bifrost_cmd):
        self.pipe = subprocess.Popen(bifrost_cmd,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True,
                                     close_fds=True)

    def import_module(self, module_name):
        return self.get_result({'module': module_name})

    def callmethod(self, oid, method, params):
        return self.get_result({
            'oid': oid,
            'method': method,
            'params': [self.deproxify(param) for param in params]
        })

    def get_result(self, request):
        message = json.dumps(request).encode('utf-8')
        self.pipe.stdin.write(message + b'\n')
        self.pipe.stdin.flush()
        line = self.pipe.stdout.readline().decode('utf-8')
        result = json.loads(line)
        if 'error' in result:
            raise RuntimeError(result['error'])
        if 'result' not in result:
            raise RuntimeError('no result')
        return self.proxify(result['result'])

    def deproxify(self, obj):
        if isinstance(obj, (int, float, str, bool)) or obj is None:
            return obj
        if isinstance(obj, Proxy):
            return {'__oid__': obj.oid}
        if isinstance(obj, dict):
            return {self.deproxify(key): self.deproxify(val)
                    for key, val in obj.items()}
        if isinstance(obj, collections.abc.Iterable):
            return [self.deproxify(item) for item in obj]

        raise RuntimeError('unexpected obj for deproxify')

    def proxify(self, obj):
        if isinstance(obj, (int, float, str, bool)) or obj is None:
            return obj
        if isinstance(obj, dict):
            if '__oid__' in obj:
                return Proxy(obj['__oid__'], self)
            return {self.proxify(key): self.proxify(val)
                    for key, val in obj.items()}
        if isinstance(obj, collections.abc.Iterable):
            return [self.proxify(item) for item in obj]

        raise RuntimeError('unexpected obj for proxify')
