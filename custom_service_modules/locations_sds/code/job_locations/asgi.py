import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
import django
import zmq
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_locations.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
    }
)

import state_model.state_model
import shoestring_wrapper.wrapper

zmq_config = {
    "wrapper_out": {
        "type": zmq.PUSH,
        "address": "tcp://127.0.0.1:6000",
        "bind": True,
    },
    "state_in": {
        "type": zmq.PULL,
        "address": "tcp://127.0.0.1:6000",
        "bind": False,
    },
    "state_out": {
        "type": zmq.PUSH,
        "address": "tcp://127.0.0.1:6001",
        "bind": False,
    },
    "wrapper_in": {
        "type": zmq.PULL,
        "address": "tcp://127.0.0.1:6001",
        "bind": True,
    },
}

# shoestring_wrapper.wrapper.Wrapper.start({'zmq_config':zmq_config})
shoestring_wrapper.wrapper.MQTTServiceWrapper(settings.MQTT, zmq_config).start()
state_model.state_model.StateModel(zmq_config).start()
