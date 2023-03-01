import json
import logging

from django.http import HttpRequest, JsonResponse
from asgiref.sync import async_to_sync, sync_to_async
from django.views.decorators.csrf import csrf_exempt
from aiogram import Router, Bot, Dispatcher
from aiogram.types.update import Update


update_router = Router()
@sync_to_async
@csrf_exempt
@async_to_sync
async def update(request: HttpRequest):
    if request.method == 'POST':
        json_string = request.body
        update = Update(**json.loads(json_string.decode('utf-8')))
        bot = Bot.get_current()
        # обращение к родительскому роуту - диспетчеру
        dispatcher = update_router._parent_router
        await dispatcher.feed_update(bot=bot, update=update)
        return JsonResponse({"status": "OK"}, status=200)
    return JsonResponse({"status": "I`m a teapot"}, status=418)
