import webtest

import greetings_api


def test_get():
    app = webtest.TestApp(greetings_api.app)

    response = app.get('/v1/greetings/greetings')

    assert response.status_int == 200
    assert response.body.json['message'] == 'hello-world'
