from django.test.client import Client as TestClient

class Client(TestClient):
    def options(self, *args, **kwargs):
        return super(Client, self).options(*args, **kwargs)

    def post(self, *args, **kwargs):
        return super(Client, self).post(*args, **kwargs)

    def get(self, *args, **kwargs):
        return super(Client, self).get(*args, **kwargs)

    def put(self, *args, **kwargs):
        return super(Client, self).put(*args, **kwargs)

    def head(self, *args, **kwargs):
        return super(Client, self).head(*args, **kwargs)

    def trace(self, *args, **kwargs):
        return super(Client, self).trace(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return super(Client, self).connect(*args, **kwargs)
