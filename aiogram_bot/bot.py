from .config import settings
from .application import AiogramApp
from .handlers import router
from transmitter.views import update_router


TOKEN = settings.BOT_TOKEN.get_secret_value()
routes = [update_router, router]
app = AiogramApp(token=TOKEN, debug=settings.DEBUG)
app._download_routes(routes=routes)
