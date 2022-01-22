from smartapp.redis import redis
import signal
from typing import List

class PubSub(redis.Redis):

    groups = {}

    @classmethod
    def new_group(cls, name: str, chans: List[str]):
        cls.groups[name] = chans

    def __init__(self):
        super().__init__()
        self._chan = self.pubsub()
        self.thread = None
        self.subscribed = []
        self._terminating = False

    def stop(self):
        self.thread.stop()
        self.thread.join(timeout=1.0)
        self.thread = None
        self._chan.close()

    def sub(self, chan, handler):
        self._chan.subscribe(**{chan: handler})
        self.subscribed.append(chan)

    def pub(self, chan, body):
        self.publish(chan, body)

    def channels(self):
        return self._chan.pubsub_channels()

    def sig_handle(self, sig, frame):
        if not self._terminating:
            self._terminating = True
            self.stop()

    def start(self):
        signal.signal(signal.SIGINT, self.sig_handle)
        signal.signal(signal.SIGTERM, self.sig_handle)
        self.thread = self._chan.run_in_thread(sleep_time=0.1)
