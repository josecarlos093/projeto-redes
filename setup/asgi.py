from fast_api.main import app as fast_api
from django.core.asgi import get_asgi_application
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.applications import Starlette
from starlette.routing import Mount
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

django_app = get_asgi_application()

application = Starlette(routes=[
    Mount("/django", WSGIMiddleware(django_app)),
    Mount("/api", fast_api),
])
