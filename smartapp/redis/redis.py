import typing
import redis
import smartapp

class RedisMeta(typing._ProtocolMeta):

    @property
    def config(cls):
        return smartapp.config.redis


class Redis(redis.Redis, metaclass=RedisMeta):

    _pool = None

    @classmethod
    def get_pool(cls):
        if not cls._pool:
            if not cls.config:
                return
            cls._pool = redis.ConnectionPool(**cls.config)
        return cls._pool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
            connection_pool=self.__class__.get_pool(),
        )

    def do(self, *args, **kwargs):
        return self.execute_command(*args, **kwargs)
