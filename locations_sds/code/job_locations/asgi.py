import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
import django
# from channels.layers import get_channel_layer

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
                'inbound_topic':'wrapper_in',
                'outbound_topic':'wrapper_out',
                'pub_ep':'tcp://127.0.0.1:6000',
                'sub_ep':'tcp://127.0.0.1:6001',
                }

shoestring_wrapper.wrapper.Wrapper.start({'zmq_config':zmq_config})
state_model.state_model.StateModel(zmq_config).start()
