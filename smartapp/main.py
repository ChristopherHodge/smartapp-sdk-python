import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
import sys
import json
import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse

from smartapp import logger
log = logger.get()

from smartapp import version
from smartapp import rest

if 'IS_TEST' in os.environ:
    version.__version__ = '1.2.3'

if 'PRODUCTION' not in os.environ:
    sys.dont_write_bytecode = True

app = fastapi.FastAPI(
    title='smartapp',
    version=version.__version__
)

def include_routes():
    app.include_router(rest.version.router, tags=['Version'])
    app.include_router(rest.smartapp.router, tags=['SmartApp'])

@app.on_event('startup')
async def startup():
    include_routes()

@app.on_event('shutdown')
async def shutdown():
    pass

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    log.error(str(exc))
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(exc.errors())
    )
