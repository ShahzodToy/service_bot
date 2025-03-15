import logging

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup 

from utils.filters import AdminFilter
from keyboards.reply import rp_keyboard
from database import service

class AddService(StatesGroup):
    service_category = State()
    service_name = State()
    description = State()

ADMIN_IDS = [5714872865]

admin_router = Router()

admin_router.message.filter(AdminFilter(admin_ids=ADMIN_IDS))

@admin_router.message(CommandStart())
async def run_as_admin(message:Message):
    await message.answer('Xush kelibsiz admin bo\'limiga', reply_markup=rp_keyboard.admin_menu)

@admin_router.message(StateFilter(None),F.text.in_(['Barcha buyurtmalar']))
async def get_all_orders(message:Message):
    orders = await service.get_all_order_admin()
    if not orders:
        await message.answer('Sizda xali buyurtmalar mavjud emas', reply_markup=rp_keyboard.admin_menu)
        return
    
    order_texts = [
        f"📌 Xizmat turi: {order.service.name}\n"
        f"👤 Toliq ism: {order.full_name}\n"
        f"📞 Telefon raqam: {order.phone_number}\n"
        f"📍 Manzil: {order.location}\n"
        f"----------------------"
        for order in orders
    ]

    result_text = "\n".join(order_texts)

    if result_text.strip():  
        await message.answer(result_text)
    else:
        await message.answer('Sizda hali buyurtmalar mavjud emas', reply_markup=rp_keyboard.admin_menu)
        

@admin_router.message(StateFilter(None),F.text.in_(['Xizmatlar qo\'shish']))
async def add_extra_service(message:Message, state:FSMContext):
    await message.answer('Xizmat kategoriyasini tanglang yoki qo\'ldakiriting', reply_markup=await service.get_all_service_category_keyboard_admin())
    await state.set_state(AddService.service_category)

@admin_router.message(AddService.service_category)
async def create_or_get_category_servcie(message:Message, state:FSMContext):
    await state.update_data(service_category=message.text)
    category_service = await service.get_category_service_name(message.text)
    if category_service == None:
        await service.create_category_service_name(message.text)
    await message.answer('Xizmat nomini kiriting:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddService.service_name)

@admin_router.message(AddService.service_name)
async def create_new_category(message:Message, state:FSMContext):
    await state.update_data(service_name=message.text)
    await message.answer('Xizmatga taluqli kommentariya yozing')
    await state.set_state(AddService.description)

@admin_router.message(AddService.description)
async def create_new_service_descrip(message:Message, state:FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    category_service = await service.get_category_service_name(data['service_category'])
    logging.info(category_service)
    await state.update_data(service_category=category_service.id)
    data = await state.get_data()
    await service.create_new_service(name=data['service_name'],
                                     category_id=data['service_category'],
                                     description=data['description'])

    await message.answer('Xizmat muvvaffaqiyatli yaratildi!!', reply_markup=rp_keyboard.admin_menu)
    await state.clear()

