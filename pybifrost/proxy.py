class Proxy:

    def __init__(self, oid, bifrost):
        self.oid = oid
        self.bifrost = bifrost

    def __getattr__(self, name):
        def method_proxy(*args):
            return self.bifrost.callmethod(self.oid, name, args)
        return method_proxy
