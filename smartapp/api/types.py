import pydantic
import fastapi
from typing import Optional

class AppRequest(fastapi.Request):
    pass

class AppCtx(pydantic.BaseModel):
    app_id:        Optional[str]
    location_id:   Optional[str]
    token:         Optional[str]
    refresh_token: Optional[str]
    secret:        Optional[str]

class AppCtxError(Exception):
    pass

class AuthInvalid(Exception):
    pass

class AppHTTPError(fastapi.HTTPException):
    pass
