import sys
import logging
import inspect

from logging import INFO, WARN, ERROR, DEBUG

FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s] [%(item)s:%(lineno)d] %(message)s'
DATE_FMT = '%Y-%m-%d %H:%M:%S %z'

class LoggerError(Exception):
    pass

class Logger(object):

    instance = None

    def __init__(self, item):
        self.item = item

    def xtra(self):
        return {'item': self.item}

    def info(self, *args):
        self.__class__.instance.info(*args, extra=self.xtra())

    def warn(self, *args):
        self.__class__.instance.warn(*args, extra=self.xtra())

    def error(self, *args):
        self.__class__.instance.error(*args, extra=self.xtra())

    def debug(self, *args):
        self.__class__.instance.debug(*args, extra=self.xtra())


def init(service, level=INFO):
    if Logger.instance:
        raise LoggerError('logger can only be initialized once')
    logger = logging.getLogger(service)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FMT))
    logger.addHandler(sh)
    logger.setLevel(level)
    Logger.instance = logger

def get():
    if not Logger.instance:
        raise LoggerError('logger must be initialized first')
    return Logger(inspect.getmodule(inspect.stack()[1][0]).__name__)
