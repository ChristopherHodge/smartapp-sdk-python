import asyncio
import aiohttp
import fastapi
import pydantic
import functools
import traceback
from typing import Callable, Any

from smartapp.api import types

from smartapp import logger
log = logger.get()

DEFAULT_TIMEOUT=10.0

class AppTask(object):
    """Create a new AppTask instance.  Provides a convenient way
    to run a particular function as an async task, handling basic
    plubming like timeouts, exceptions, logging, etc.

    Args:
        func (Callable): function to call
        args (list): call args
        kwargs (dict): call kwargs
    """

    loop = asyncio.get_event_loop()

    @staticmethod
    def handle_excs(func: Callable) -> Callable:
        """(**decorator**) Provides a standard set of exception handlers
        to deal with many of the potentially expected scenarios, as
        well as some useful logging of unhandled types before they escape
        the app an enter the FastAPI runtime.

        This should generally be applied to any entrypoint to the SmartApp
        from a route or lifecycle.
        """

        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except types.AuthInvalid:
                return await self.renew_token()
            except pydantic.ValidationError as e:
                return log.error(e.json())
            except aiohttp.ClientResponseError as e:
                return log.error("invalid HTTP response: ", e.reason)
            except aiohttp.ClientConnectionError as e:
                return log.error("connection error: ", e.reason)
            except fastapi.HTTPException as e:
                raise e
            except Exception:
                log.error("unexpected error: %s", traceback.format_exc())
        return wrapper

    @classmethod
    def async_callable(cls, func: Callable,
                            timeout: int=DEFAULT_TIMEOUT) -> Callable:
        """(**decorator**) When called, the decorated function will return
        a Callable, which when called will execute as an async task,
        preserving any arguments used.

        This allows you to decorate a SmartApp Route handler to create an
        async route.
        """
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            coro = asyncio.wait_for(
                func(self, *args, **kwargs), timeout=timeout
            )

            task = cls.loop.create_task(coro)
            task.add_done_callback(cls.done)
        return wrapper

    @classmethod
    def async_task(cls, self, func: Callable, *args,
                              timeout=DEFAULT_TIMEOUT, **kwargs) -> Any:
        """(**decorator**) When called, the decorated function will execute
        as an asynchronous task.  Args may be passed to the function by
        the decorator.

        Useful for internal SmartApp methods which are perofmring API
        interactions which are not required to be synchronous.
        """
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            coro = asyncio.wait_for(
                func(self, *args, **kwargs), timeout=timeout
            )

            task = cls.loop.create_task(coro)
            task.add_done_callback(cls.done)
        return wrapper(self, *args, **kwargs)

    def __new__(cls, func: Callable, *args,
                     timeout=DEFAULT_TIMEOUT, **kwargs) -> None:
        coro = asyncio.wait_for(
            func(*args, **kwargs), timeout=timeout
        )

        task = cls.loop.create_task(coro)
        task.add_done_callback(cls.done)
        asyncio.ensure_future(task, loop=cls.loop)
        return task

    @staticmethod
    def done(task):
        exc = task.exception()
        if exc:
            msg = str(exc)
            if exc.__dict__:
                msg = str(exc.__dict__)
            log.error("AppTask: %s: %s", exc.__class__.__name__, msg)
            if isinstance(exc, types.AppHTTPError):
                return
            if exc.__traceback__:
                msg = traceback.format_exception(type(exc), exc, exc.__traceback__)
                log.error("AppTask: %s", str().join(msg))
        else:
            task.result()
