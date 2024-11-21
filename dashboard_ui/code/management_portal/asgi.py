import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import django
from channels.layers import get_channel_layer
import shoestring_wrapper.wrapper
import dashboard.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management_portal.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(dashboard.routing.websocket_urlpatterns))
        ),
    }
)

shoestring_wrapper.wrapper.Wrapper.start({'channel_layer':get_channel_layer()})
