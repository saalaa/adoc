import webtest

import hello_world_api


def test_get():
    app = webtest.TestApp(hello_world_api.app)

    response = app.get('/')

    assert response.status_int == 200
    assert response.body == 'Hello, World!'
