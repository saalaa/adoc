from flask import Flask, jsonify
from marshmallow import (
    Schema, fields
)


class StatusResponse(Schema):
    status = fields.String(required=True)


app = Flask(__name__)


@app.route('/api/status')
def api_status():
    """API status endpoint.

    API endpoinnt that returns the current status of the API.

    ---
    post:
      operationId: api_status
      description: >
        API status endpoint.
      responses:
        200:
          description: Moodboard image
          schema: StatusResponse
    """
    data = {
        'status': 'ok'
    }

    return jsonify(
        StatusResponse().dump(data).data
    )


if __name__ == '__main__':
    import json

    from apispec import APISpec
    from apispec.ext.flask import FlaskPlugin
    from apispec.ext.marshmallow import MarshmallowPlugin

    spec = APISpec(
        title='Flask project',
        version='v1',
        openapi_version='2.0',
        host='example.com',
        basePath='/api',
        schemes=[
            'https'
        ],
        consumes=[
            'application/json'
        ],
        produces=[
            'application/json'
        ],
        plugins=[
            FlaskPlugin(), MarshmallowPlugin()
        ]
    )

    spec.definition('StatusResponse', schema=StatusResponse)

    with app.test_request_context():
        spec.add_path(view=api_status)

    spec = spec.to_dict()

    print(
        json.dumps(spec, indent=2)
    )
