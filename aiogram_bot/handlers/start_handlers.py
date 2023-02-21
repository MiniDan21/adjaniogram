from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.text import Text
from aiogram.filters.command import CommandStart, Command
from django.core.cache import cache

from ..keyboard import build_order_keyboard


start_router = Router()

service_names_keyboard = None
back_to_service_keyboard = None

start_text = "Приветствую, {user}! Выбери одну из услуг:"

@start_router.message(CommandStart())
async def cmd_start(msg: Message):
    global service_names_keyboard, back_to_service_keyboard
    service_names_keyboard, back_to_service_keyboard = await build_order_keyboard(cache=cache)
    await msg.answer(
        text=start_text.format(user=msg.from_user.full_name),
        reply_markup=service_names_keyboard()
    )

@start_router.message(Command('restart'))
async def cmd_restart(msg: Message, bot: Bot):
    chat_id = msg.from_user.id
    for message_id in range(msg.message_id+1):
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        except TelegramBadRequest:
            pass


@start_router.callback_query(Text(startswith='service_'))
async def callbacks_service(callback: CallbackQuery, bot: Bot):
    service_names_keyboard, back_to_service_keyboard = await build_order_keyboard(cache=cache)
    codes = callback.data.split('_')
    keyboards = {
        True: service_names_keyboard,
        False: back_to_service_keyboard,
    }
    # Необходимые данные для отдельного изменения inline_keyboard
    msg_id = callback.message.message_id
    chat_id = callback.message.chat.id
    # Вывод подробного описания услуги
    if codes[-1] != 'back':
        info = await cache.aget(key='_'.join(codes[0:2]), version=2, default='Произошла ошибка. Напишите /report.')
        await callback.message.edit_text(text=info)
    # Возврат к начальному сообщению
    elif codes[-1] == 'back':
        await callback.message.edit_text(text=start_text.format(user=callback.from_user.full_name))
    await callback.answer()
    # Изменение с помощью bot, из-за изменения inline_keyboard до callback.answer()
    await bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=msg_id,
        reply_markup=keyboards[codes[-1] == 'back']()
    )


# Изюминка бота в общении через одно сообщение
# p.s. уточнить, что то можно писать кроме /start, или заблочить возможность писать больше 1 раза /start
@start_router.message(lambda m: True)
async def delete_msgs(msg: Message):
    await msg.delete()
