from smartapp import api

def http_error(status_code):
    raise api.AppHTTPError(status_code=status_code)