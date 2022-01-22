import fastapi

from smartapp.api import models
from smartapp import version

URI_BASE='/version'
router = fastapi.APIRouter()


@router.get(URI_BASE, response_model=models.Version)
def get_version():
    return {'version': version.__version__}
