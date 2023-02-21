from typing import Tuple

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from django.core.cache import cache


async def build_order_keyboard(cache, pay: bool = False):
    serv = 1
    name = True
    services = InlineKeyboardBuilder()
    back_or_pay = InlineKeyboardBuilder()
    while name:
        key = 'service_' + str(serv)
        name = await cache.aget(key=key, default=False, version=1)
        if not name:
            break
        service_buttons = [
            InlineKeyboardButton(text=name, callback_data='pay_' + key),
            InlineKeyboardButton(text='Подробнее', callback_data=key)
        ]
        services.row(*service_buttons)
        serv += 1
    if pay:
        back_or_pay.add(InlineKeyboardButton(text='Оплатить', pay=pay))
    else:
        back_or_pay.add(InlineKeyboardButton(text='Назад', callback_data='service_back'))

    return services.as_markup, back_or_pay.as_markup
