from __future__ import annotations
import signal
import fastapi

from smartapp import redis
from smartapp.api import models, smartapp
from typing import Callable, List

from smartapp import logger
log = logger.get()

router = None

class Option(dict):

    def __init__(self, name, id):
        super().__init__()
        self['name'] = name
        self['id'] = id


class Setting(models.smartapp.PageSetting):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = []
        self.permissions = ['r','w','x']

    def option(self, name=None, id=None) -> type[Setting]:
        self.options.append(Option(name, id))
        self.options[len(self.options)-1]
        return self

    def has_multiple(self, val: bool) -> type[Setting]:
        self.multiple = val
        return self

    def with_capabilities(self, val: List[str]) -> type[Setting]:
        self.capabilities = val
        return self


class Section(models.smartapp.PageSection):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = []

    def setting(self, name: str, id: str, type: models.smartapp.PageSettingType,
                multiple: bool=False, required: bool=False, **kwargs) -> List[Setting]:
        self.settings.append(
                Setting(name=name, id=id, type=type, multiple=multiple ,required=required, **kwargs)
        )
        idx = len(self.settings)-1
        log.info("add settings with index {} to section {}".format(idx, self.name))
        return self.settings[idx]


class Page(models.smartapp.PageData):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sections = []

    def reset(self):
        while len(self.sections):
            self.sections.pop()

    def section(self, name=None) -> List[Section]:
        self.sections.append(Section(name=name))
        idx = len(self.sections)-1
        log.info("page {}: add section with index {}".format(self.pageId, idx))
        return self.sections[idx]

    def render(self, body: Callable):
        self.render_func = body


class Route(object):

    def __init__(self, verb: str, path: str, func: str):
        self.verb = verb
        self.path = path
        self.func = func
        self.app  = None
        self.auth = None

    def set_auth_handler(self, func: str) -> type[Route]:
        self.auth = func
        return self

    def register(self):
        handler = getattr(self.app, self.func)
        path = '/{}{}'.format(self.app.app_id, self.path)

        kwargs = {'path': path,
                  'methods': [self.verb],
                  'endpoint': handler}

        if self.auth:
            auth = getattr(self.app, self.auth)
            auth = fastapi.Depends(auth)
            kwargs.update({'dependencies': [auth]})
        router.add_route(**kwargs)
