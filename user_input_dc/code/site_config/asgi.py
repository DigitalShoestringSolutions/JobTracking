import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import django
from django.conf import settings
import shoestring_wrapper.wrapper
import input.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_config.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(input.routing.websocket_urlpatterns))
        ),
    }
)

import zmq

zmq_config = {
    "wrapper_out": {
        "type": zmq.PUB,
        "address": "tcp://127.0.0.1:6000",
        "bind": True,
    },
    "wrapper_in": {
        "type": zmq.PULL,
        "address": "tcp://127.0.0.1:6001",
        "bind": True,
    },
}

shoestring_wrapper.wrapper.MQTTServiceWrapper(settings.MQTT, zmq_config).start()

