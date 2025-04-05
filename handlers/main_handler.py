import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart ,StateFilter
from aiogram.types import Message, ReplyKeyboardRemove

from database import service
from keyboards.reply import rp_keyboard
from utils.transaltion import translate as __
from utils.transaltion import translations
from database import models


main_router = Router()

class UserLang(StatesGroup):
    lang = State()

class UserLangChange(StatesGroup):
    lang = State()

class OrderService(StatesGroup):
    service_category = State()
    service = State()
    calculate = State()
    order_way = State()
    full_name = State()
    phone_number = State()
    location = State()
    veriy = State()

    texts = {
        "OrderService:service_category": {
            "en": "Choose service category",
            "uz": "Xizmat turini tanlang",
            "ru": "Выберите категорию услуги"
        },
        "OrderService:service": {
            "en": "Choose service type:",
            "uz": "Xizmat turini tanlang:",
            "ru": "Выберите тип услуги:"
        },
        "OrderService:order_way": {
            "en": "Choose the way of communication",
            "uz": "Aloqa usulini tanlang",
            "ru": "Выберите способ связи"
        },
        "OrderService:full_name": {
            "en": "Enter name once more:",
            "uz": "Ism va familiyani qayta kiriting:",
            "ru": "Введите имя еще раз:"
        },
        "OrderService:phone_number": {
            "en": "Enter phone number once more",
            "uz": "Telefon raqamini qayta kiriting",
            "ru": "Введите номер телефона еще раз"
        },
        "OrderService:location": {
            "en": "Enter location once more",
            "uz": "Manzilni qayta kiriting",
            "ru": "Введите местоположение еще раз"
        },
        "OrderService:veriy": {
            "en": "Enter verification:",
            "uz": "Tasdiqlash kodini kiriting:",
            "ru": "Введите код подтверждения:"
        },
    }

@main_router.message(StateFilter(None), CommandStart())
async def command_start_handler(message: Message, state:FSMContext):
    user_ = await service.get_user_id(message.from_user.id)
    logging.info(user_)
    if user_ is not None:  
        await message.answer(__("Welcome to our main page", user_.language), 
                             reply_markup=rp_keyboard.main_menu(user_.language))
    else:
        await state.set_state(UserLang.lang)
        await message.answer('Choose language/Til tanlang/Выберите язык', 
                             reply_markup=rp_keyboard.lang_menu)

@main_router.message(UserLang.lang, F.text)
async def setting_language(message: Message, state:FSMContext):
    languages = {
        '🇬🇧 English': "en",
        '🇺🇿 Uzbek': "uz",
        '🇷🇺 Russian': "ru"
    }
    if message.text not in languages:
        await message.answer("Faqatgina kerakli tilni tanglang")
        return  
    await state.update_data(lang = languages[message.text])
    user = await state.get_data()
    await service.create_user(telegram_id=message.from_user.id, lang=user['lang'])
    user_ = await service.get_user_id(message.from_user.id)
    await message.answer(__("Welcome to our main page", user_.language), reply_markup=rp_keyboard.main_menu(user_.language))

    await state.clear()

@main_router.message(StateFilter(None),F.text.in_(['Services','Услуги','Xizmatlar']), F.text)
async def get_all_services_category(message:Message, state: FSMContext):
    user_ = await service.get_user_id(message.from_user.id)
    await state.set_state(OrderService.service_category)
    await message.answer(__('Choose service category',user_.language), reply_markup= await service.get_all_service_category_keyboard(user_.language))

@main_router.message(F.text.in_(['My Orders','Мои заказы','Mening buyurtmalarim']))
async def get_all_orders(message:Message):
    orders = await service.get_all_order(telegram_id=message.from_user.id)
    user_ = await service.get_user_id(message.from_user.id)
    if not orders:
        await message.answer(__("You have no orders yet.",user_.language))
        return
    
    order_texts = [
        f"📌 {translations['service_name'][user_.language]}: {getattr(order.service, f'name_{user_.language}', 'Unknown')}\n"
        f"👤 {translations['full_name'][user_.language]}: {order.full_name}\n"
        f"📞 {translations['phone_number'][user_.language]}: {order.phone_number}\n"
        f"📍 {translations['location'][user_.language]}: {order.location}\n"
        f"----------------------"
        for order in orders
    ]

    await message.answer("\n".join(order_texts))

@main_router.message(OrderService.service_category,~F.text.in_(['⬅️ Back','⬅️ Orqaga','⬅️ Назад']))
async def get_all_service(message:Message, state:FSMContext):
    user_ = await service.get_user_id(message.from_user.id)
    await state.update_data(service_category=message.text)
    await message.answer(__('Choose services',user_.language), reply_markup= await service.get_service_by_name_keyboard(message.text,user_.language))
    await state.set_state(OrderService.service)

@main_router.message(OrderService.service,~F.text.in_(['⬅️ Back','⬅️ Orqaga','⬅️ Назад']))
async def choose_order_way(message:Message, state:FSMContext):
    await state.update_data(service=message.text)
    user_ = await service.get_user_id(message.from_user.id)
    service_data = await service.get_service_by_name(message.text,user_.language)
    if service_data:
        description = getattr(service_data, f"description_{user_.language}", "No description available")
    else:
        description = "Service not found."
    await message.answer(description, reply_markup=rp_keyboard.order_way(user_.language))
    if service_data.calculate:
        await message.answer(__("O'lchovni kiriting",user_.language),reply_markup=ReplyKeyboardRemove())
        await state.set_state(OrderService.calculate)
    else:
        await message.answer(__('Narxi:',user_.language)+str(service_data.price), reply_markup=rp_keyboard.order_way(user_.language))
        await state.set_state(OrderService.order_way)

@main_router.message(OrderService.calculate, ~F.text.in_(['⬅️ Back','⬅️ Orqaga','⬅️ Назад']))
async def calculate_price_service(message:Message, state:FSMContext):
    user_ = await service.get_user_id(message.from_user.id)
    service_name = await state.get_data()
    service_data = await service.get_service_by_name(service_name['service'],user_.language)
    calculation = int(service_data.price) * int(message.text) 
    await message.answer(__('Narxi:',user_.language)+str(calculation),reply_markup=rp_keyboard.order_way(user_.language))
    await state.set_state(OrderService.order_way)

@main_router.message(OrderService.order_way, ~F.text.in_(['⬅️ Back','⬅️ Orqaga','⬅️ Назад']))
async def get_contact_phone(message:Message, state:FSMContext):
    await state.update_data(order_way=message.text)
    user_ = await service.get_user_id(message.from_user.id)
    if message.text in ['📞 Phone number','📞 Telefon raqami','📞 Номер телефона']:
        await message.answer(__('Contact our poeple: +998949252945',user_.language), reply_markup=rp_keyboard.main_menu(user_.language))
        await state.clear()
    else:
        await message.answer(__('Enter your full name',user_.language),reply_markup=rp_keyboard.back_keyboard(user_.language))
        await state.set_state(OrderService.full_name)

@main_router.message(OrderService.full_name, ~F.text.in_(['⬅️ Back','⬅️ Orqaga','⬅️ Назад']))
async def get_fullname(message:Message, state:FSMContext):
    user_ = await service.get_user_id(message.from_user.id)
    await state.update_data(full_name=message.text)
    await message.answer(__('Enter your valid phone number',user_.language), reply_markup=rp_keyboard.phone_numbe_keyboard(user_.language))
    await state.set_state(OrderService.phone_number)

@main_router.message(OrderService.phone_number, ~F.text.in_(['⬅️ Back','⬅️ Orqaga','⬅️ Назад']))
async def get_valid_phone_number(message:Message, state:FSMContext):
    user_ = await service.get_user_id(message.from_user.id)
    await state.update_data(phone_number = message.contact.phone_number)
    await message.answer(__('Please provide your full location!!!',user_.language), reply_markup=rp_keyboard.back_keyboard(user_.language))
    await state.set_state(OrderService.location)

@main_router.message(OrderService.location, ~F.text.in_(['⬅️ Back','⬅️ Orqaga','⬅️ Назад']))
async def get_valid_location(message:Message, state:FSMContext):
    await state.update_data(location = message.text)
    user_ = await service.get_user_id(message.from_user.id)
    data = await state.get_data()
    logging.info(data)
    if user_.language =='en':
        await message.answer(
                            f"Service category: {data['service_category']}\n"
                            f"Service: {data['service']}\n"
                            f"Full Name: {data['full_name']}\n"
                            f"Phone Number: {data['phone_number']}\n"
                            f"Location: {data['location']}",
                            reply_markup=rp_keyboard.verify_order_keyboard(user_.language)
        )
    elif user_.language == 'uz':
        await message.answer(
            f"Xizmat kategoriyasi: {data['service_category']}\n"
            f"Xizmat: {data['service']}\n"
            f"Ism Familiya: {data['full_name']}\n"
            f"Telefon raqam: {data['phone_number']}\n"
            f"Manzil: {data['location']}",
            reply_markup=rp_keyboard.verify_order_keyboard(user_.language)
        )
    else:
        await message.answer(
            f"Категория услуги: {data['service_category']}\n"
            f"Услуга: {data['service']}\n"
            f"ФИО: {data['full_name']}\n"
            f"Номер телефона: {data['phone_number']}\n"
            f"Местоположение: {data['location']}",
            reply_markup=rp_keyboard.verify_order_keyboard(user_.language)
)

    await state.set_state(OrderService.veriy)

@main_router.message(OrderService.veriy, ~F.text.in_(['⬅️ Back','⬅️ Orqaga','⬅️ Назад']))
async def get_verify_order(message:Message, state:FSMContext):
    user = await service.get_user_id(user_id=message.from_user.id)

    if message.text in ['❌ Cancel order','❌ Отменить заказ','❌ Buyurtmani bekor qilish']:
        await state.clear()
        await message.answer(__('Order cancelled successfully',user.language), reply_markup=rp_keyboard.main_menu(user.language))
        return
    data = await state.get_data()
    service_ = await service.get_service_by_name(data['service'],user.language)

    await service.create_new_order(full_name=data['full_name'],
                                   phone_number=data['phone_number'],
                                   location=data['location'],
                                   user_id=user.id,
                                   service_id=service_.id,
                                   )
    await message.answer(__('Order created successfully',user.language), reply_markup=rp_keyboard.main_menu(user.language))
    await state.clear()

@main_router.message(F.text.in_(['⚙️ Settings','⚙️ Настройки','⚙️ Sozlamalar']))
async def menu_settings(message:Message):
    user = await service.get_user_id(user_id=message.from_user.id)
    await message.answer(__('Settings menu',user.language),reply_markup=rp_keyboard.setting_menu(user.language))

@main_router.message(StateFilter(None), F.text.in_(['Change Language',"Tilni o'zgartirish",'Изменить язык']))
async def language_settings(message:Message, state:FSMContext):
    user = await service.get_user_id(user_id=message.from_user.id)
    await message.answer(__('Choose langugae!!',user.language), reply_markup=rp_keyboard.lang_menu)
    await state.set_state(UserLangChange.lang)

@main_router.message(UserLangChange.lang)
async def change_language_settings(message:Message,state:FSMContext):
    user_lang = await service.get_user_id(user_id=message.from_user.id)
    user = await service.change_language(telegram_id=message.from_user.id, lang=user_lang.language)
    languages = {
        '🇬🇧 English': "en",
        '🇺🇿 Uzbek': "uz",
        '🇷🇺 Russian': "ru"
    }
    if message.text not in languages:
        await message.answer(__("Please choose only one of the languages",user.language))
        return
    user_ = await service.change_language(telegram_id=message.from_user.id, lang=languages[message.text])
    await message.answer(__('Language updated successfully',user.language),reply_markup=rp_keyboard.main_menu(user_.language))
    await state.clear()

@main_router.message(StateFilter('*', F.text.in_(['⬅️ Back','⬅️ Orqaga','⬅️ Назад'])))
async def back_previous(message:Message, state:FSMContext):
    current_state = await state.get_state()
    user = await service.get_user_id(user_id=message.from_user.id)
    if current_state == OrderService.service_category:
        await message.answer(__("Welcome to our main page", user.language), 
                             reply_markup=rp_keyboard.main_menu(user.language))
        await state.clear()
        
        return 
    previous = None
    for step in OrderService.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            if previous == OrderService.service_category:
                keyboard = await service.get_all_service_category_keyboard(user.language)
            elif previous == OrderService.service:
                user_data = await state.get_data()
                keyboard = await service.get_service_by_name_keyboard(user_data.get("service_category"),user.language)
            elif previous == OrderService.order_way:
                keyboard = rp_keyboard.order_way(user.language)
            elif previous == OrderService.full_name:
                keyboard = rp_keyboard.back_keyboard(user.language)
            elif previous == OrderService.phone_number:
                keyboard = rp_keyboard.phone_numbe_keyboard(user.language)
            elif previous == OrderService.location:
                keyboard = rp_keyboard.back_keyboard(user.language)
            elif previous == OrderService.veriy:
                keyboard = rp_keyboard.verify_order_keyboard(user.language)
            else:
                keyboard = ReplyKeyboardRemove()
            await message.answer(
                f"{OrderService.texts[previous.state][user.language]}", reply_markup=keyboard
            )
            return 
        previous = step

