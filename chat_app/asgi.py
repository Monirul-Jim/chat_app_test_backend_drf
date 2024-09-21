"""
ASGI config for chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

# application = get_asgi_application()
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from signup_login import routing as chat_routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat_routing.websocket_urlpatterns
#         )
#     ),
# })
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import signup_login.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             signup_login.routing.websocket_urlpatterns
#         )
#     ),
# })
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from signup_login import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
