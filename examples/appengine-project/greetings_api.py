import endpoints

from protorpc import (
    message_types, messages, remote
)


class Greeting(messages.Message):
    message = messages.StringField(1, required=True)


@endpoints.api(name='greetings', version='v1')
class GreetingsApi(remote.Service):
    @endpoints.method(
        message_types.VoidMessage,
        Greeting,
        path='greetings',
        http_method='GET',
        name='greetings.list'
    )
    def greetings_list(self, request):
        return Greeting(
            message='hello-world'
        )


app = endpoints.api_server([GreetingsApi])
