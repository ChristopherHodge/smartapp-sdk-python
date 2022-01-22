import fastapi

from smartapp import logger
log = logger.get()

from smartapp.api import models
from smartapp import controllers

URI_BASE = '/'
router = fastapi.APIRouter()

def respond(resp):
    if not resp:
        raise fastapi.HTTPException(status_code=404)
    return resp


@router.post(URI_BASE, response_model=models.LifecycleResponse, status_code=200,
             response_model_exclude_none=True)
async def post_lifecycle(lifecycle: models.AllLifecycles):
    ctrl = controllers.SmartApp()
    return respond(await ctrl.handle_lifecycle(lifecycle))


def add_route(*args, **kwargs):
    router.add_api_route(*args, **kwargs)
