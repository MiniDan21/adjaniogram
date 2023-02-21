from aiogram import types, Bot, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters.text import Text
from django.core.cache import cache
from transmitter.models import Order, Service

from .start_handlers import start_router, build_order_keyboard
from ..config import settings


router = Router()


# После нажатия на кнопку с услугой, высвечивается окно с оплатой
@router.callback_query(Text(startswith='pay_'))
async def show_pay_window(callback: CallbackQuery, bot: Bot):
    *_, pay_for_service_keyboard = await build_order_keyboard(cache=cache, pay=True)
    codes = callback.data.split('_')
    cache_key = '_'.join(codes[1:3])
    label = await cache.aget(key=cache_key, version=1)
    # msgs = await cache.aget(key=callback.from_user.id, default=[])
    # msgs.append(callback.message.message_id+1)
    # await cache.aset(key=callback.from_user.id, value=msgs)
    # await cache.aadd(key=callback.from_user.id, value=callback.message.message_id+1)
    message = await callback.message.answer_invoice(
        title='Услуга: ' + await cache.aget(key=cache_key, version=1),
        description=await cache.aget(key=cache_key, version=2),
        provider_token=settings.PAY_TOKEN.get_secret_value(),
        currency='rub',
        is_flexible=False,  # True If you need to set up Shipping Fee
        # Проблема: добавить в бд поле с ценой
        prices=[types.LabeledPrice(
                label=label,
                amount=100*int(await cache.aget(key=cache_key, version=3))
            )],
        payload=await cache.aget(key=cache_key, version=4),
        reply_markup=pay_for_service_keyboard(),
    )
    # Для удаления кнопки с invoice
    print(message.message_id)
    await cache.aset(key=callback.from_user.id, value=message.message_id)
    await callback.answer()

# НИЖЕ ПРИМЕРЫ

@router.pre_checkout_query(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery, bot: Bot):
    chat_id = pre_checkout_query.from_user.id
    message_id = await cache.aget(key=pre_checkout_query.from_user.id)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    service_obj = Service.objects.get(pk=pre_checkout_query.invoice_payload)
    cache.delete(key=chat_id)
    Order.objects.create(user_id=chat_id, service_id=service_obj)
    await pre_checkout_query.answer(
        ok=True,
        error_message="Aliens tried to steal your card's CVV,"
                      " but we successfully protected your credentials,"
                      " try to pay again in a few minutes, we need a small rest."
            )


@router.message(F.content_type.in_(ContentType.SUCCESSFUL_PAYMENT))
async def got_payment(msg: types.Message):
    *_, back_to_service_keyboard = await build_order_keyboard(cache=cache, pay=False)
    await msg.answer(
        text='Поздравляю, покупка прошла успешно!',
        reply_markup=back_to_service_keyboard()
    )

router.include_router(router=start_router)
