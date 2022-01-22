import pytest
from smartapp.api import types
from smartapp.api.smartapp import context
from tests.conftest import test_app, client, APP_ID

def test_smartapp_version_route():
    resp = client.get('/version')
    assert resp.status_code == 200
    assert resp.json() == {'version': '1.2.3'}

@pytest.fixture(autouse=True)
def app_instance():
    app = test_app()
    app.ctx = context.AppContext.ctx(app, app_id=APP_ID)
    app.load_routes()
    return app.ctx

def test_smartapp_route1():
    resp = client.get(APP_ID + '/route1')
    assert resp.status_code == 200
    assert resp.json() == {'name': 'test_route1'}

def test_smartapp_route_slug():
    thing = 'the_thing'
    resp = client.get(APP_ID + '/route1/' + thing)
    assert resp.status_code == 200
    assert resp.json() == {'slug': thing}

def test_smartapp_route_body():
    body = {"a": "b"}
    resp = client.post(APP_ID + '/route1', json=body)
    assert resp.status_code == 200
    assert resp.json() == {'body': body}

def test_smartapp_route_not_auth():
    resp = client.get(APP_ID + '/require_auth')
    assert resp.status_code == 401

def test_smartapp_route_use_auth(app_instance):
    headers = {'Authorization': 'Bearer ' + app_instance.secret}
    resp = client.get(APP_ID + '/require_auth', headers=headers)
    assert resp.status_code == 200

def test_smartapp_route_non_exist():
    resp = client.get(APP_ID + '/nonexistent')
    assert resp.status_code == 404
