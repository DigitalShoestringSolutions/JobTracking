import os
from channels.routing import get_default_application
import django
from django.conf import settings
import shoestring_wrapper.wrapper

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management_portal.settings')
django.setup()
application = get_default_application()

import zmq

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

shoestring_wrapper.wrapper.MQTTServiceWrapper(settings.MQTT, zmq_config).start()
