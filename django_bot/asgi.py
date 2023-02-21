"""
ASGI config for django_bot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import logging

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_bot.settings')

logging.basicConfig(level=logging.INFO)


application = get_asgi_application()

# Порядок запуска приложений важен
# Для дебага в aiogram_bot/config.py DEBUG надо сделать True
from aiogram_bot import BOT_APP

bot_app = BOT_APP()
