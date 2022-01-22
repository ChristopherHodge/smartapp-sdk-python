import aiohttp
import traceback

import smartapp

from smartapp import api
from smartapp.api import types

from smartapp import logger
log = logger.get()

SCHEME = 'https'


class RESTMeta(type):

    @property
    def config(cls):
        return smartapp.config.smartthings


class RESTClient(metaclass=RESTMeta):

    def __init__(self, host, base, resource=str(), token=None, basic=None, session=None):
        self.host     = host
        self.base     = base
        self.resource = resource
        self.token    = token
        self.basic    = basic
        self.session  = session

    async def do(self, verb, endpoint, body=None, text=None, params=None):
        url = '{}:////{}{}/{}{}'.format(
            SCHEME, self.host, self.base, self.resource, endpoint
        ).replace('//','/')
        log.info("%s: %s", verb, url)
        try:
            if self.basic:
                session = aiohttp.ClientSession(headers={
                    'Authorization': 'Basic {}'.format(self.basic)
                })
            elif not self.session:
                session = api.AppContext.new_session(self.token)
            else:
                session = self.session
            async with session.request(verb, url, json=body,
                                       data=text, params=params) as resp:
                if resp.status == 401:
                    raise types.AuthInvalid()
                if resp.status < 200 or resp.status > 299:
                    log.error("response: code: %s / body: %s", resp.status, await resp.text())
                    log.error("body sent: %s", body or text)
                    raise types.AppHTTPError(status_code=resp.status)
                if text:
                    return await resp.text()
                return await resp.json()
        except aiohttp.ContentTypeError as e:
            log.error(e)
            return await resp.text()
        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                raise types.AuthInvalid()
            raise types.AppHTTPError(status_code=resp.status)
        except (types.AuthInvalid, types.AppHTTPError) as e:
            raise e
        except Exception:
            log.error(traceback.format_exc())
        finally:
            if not self.session:
                await session.close()
