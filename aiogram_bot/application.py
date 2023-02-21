import logging
# import asyncio
# import aiohttp

from aiogram import Bot, Dispatcher
from django.core.cache import cache

from .config import settings, run_async
from transmitter.models import Service, Order




class AiogramApp:
    def __init__(self, token, debug: bool) -> None:
        self.__TOKEN = token
        self.__DEBUG = debug
        self.bot = Bot(token=self.__TOKEN, parse_mode='HTML')
        Bot.set_current(self.bot)
        self.dispatcher = Dispatcher(bot=self.bot)

    async def __set_webhook(self):
        await self.bot.delete_webhook(drop_pending_updates=True)
        WEBHOOK_URL = settings.WEBHOOK_HOST + settings.WEBHOOK_PATH + settings.BOT_TOKEN.get_secret_value()
        if not await self.bot.set_webhook(url=WEBHOOK_URL, certificate=open(settings.SSL_CERTIFICATE, 'rb')):
            logging.warning('Вебхук не установлен.')
            return False
        return True

    def _download_routes(self, routes):
        head = self.dispatcher
        for route in routes:
            tail = route
            head.include_router(tail)
            head = route

    async def async_call(self):
        logging.warning('Бот запущен.')
        if self.__DEBUG:
            cache.clear()
        for service in Service.objects.all():
            cache.set(key='service_' + str(service.id), value=service.name, version=1, timeout=None)
            cache.set(key='service_' + str(service.id), value=service.description, version=2, timeout=None)
            cache.set(key='service_' + str(service.id), value=service.price, version=3, timeout=None)
            cache.set(key='service_' + str(service.id), value=service.id, version=4, timeout=None)

        await self.__set_webhook()

    def __call__(self):
        result = run_async(self.async_call)
        return self

    def __del__(self):
        logging.warning('Завершение работы бота.')
