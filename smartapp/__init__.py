import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=ImportWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

from smartapp import logger
logger.init('smartapp')

import smartapp
from smartapp import api
from smartapp import main
from smartapp import rest
from smartapp import controllers

config = None

class AppRouter(object):

    @staticmethod
    def add_route(*args, **kwargs):
        rest.smartapp.add_route(*args, **kwargs)

    @staticmethod
    def reload():
        main.app.include_router(rest.smartapp.router)

controllers.smartapp.app_ctx = api.smartapp.AppContext
api.smartapp.configuration.router = AppRouter

def init(app, config):
    smartapp.config = config
    api.smartapp.AppContext.new_app = app
    api.AppTask(controllers.smartapp.app_ctx.init)
    return main.app


__pdoc__ = {}
__pdoc__.update({'smartapp.main': False})
__pdoc__.update({'smartapp.rest': False})
#__pdoc__.update({'smartapp.controllers': False})
__pdoc__.update({'smartapp.redis': False})
__pdoc__.update({'smartapp.version': False})
__pdoc__.update({'smartapp.init': False})
__pdoc__.update({'smartapp.AppRouter': False})
__pdoc__.update({'smartapp.api.models.smartthings': False})
__pdoc__.update({'smartapp.api.http': False})
__pdoc__.update({'smartapp.api.smartthings.oauth': False})
__pdoc__.update({'smartapp.api.smartapp.task.AppTask.done': False})
__pdoc__.update({'smartapp.api.smartapp.task.AppTask.loop': False})
__pdoc__.update({'smartapp.api.smartapp.smartapp.SmartApp.pageId': False})
__pdoc__.update({'smartapp.api.smartapp.smartapp.SmartApp.load_routes': False})
__pdoc__.update({'smartapp.api.smartapp.smartapp.SmartApp.initialize': False})
__pdoc__.update({'smartapp.api.smartapp.smartapp.SmartApp.token': False})
__pdoc__.update({'smartapp.api.smartapp.smartapp.SmartApp.refresh_token': False})
__pdoc__.update({'smartapp.api.smartapp.smartapp.SmartApp.renew_token': False})
__pdoc__.update({'smartapp.api.smartapp.smartapp.SmartApp.authentication': False})
