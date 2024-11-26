import os

# imports
from channels.routing import ProtocolTypeRouter, URLRouter
from Chat import routing
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {"http": django_asgi_app, "websocket": URLRouter(routing.websocket_urlpatterns)}
)
