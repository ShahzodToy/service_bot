from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from . import models
from utils.transaltion import translate as __


async def get_user_id(user_id:int):
    async with models.async_session() as session:
        stmt = await session.execute(select(models.User).where(models.User.telegram_id==user_id))
        user = stmt.scalar_one_or_none()
        return user 
    
async def create_user(telegram_id: int, lang: str):
    async with models.async_session() as session:
        user = models.User(telegram_id=telegram_id, language=lang)
        session.add(user)
        await session.commit()

async def get_service_category():
    async with models.async_session() as session:
        stmt = await session.execute(select(models.ServiceCategory))
        service_category = stmt.scalars().all()
        return service_category
    
async def get_all_service(category_id: int):
    async with models.async_session() as session:
        stmt = await session.execute(select(models.Service).where(models.Service.service_category_id == category_id))
        service = stmt.scalars().all()
        return service
    
async def get_service_by_name_keyboard(service_category:str, lang:str):
    async with models.async_session() as session:
        category_column = getattr(models.ServiceCategory, f'name_{lang}')
        stmt = await session.execute(
            select(models.Service)
            .join(models.ServiceCategory)
            .where(category_column == service_category)
            .order_by(models.Service.created_time)
)
        services = stmt.scalars().all()
        
        keyboard = []
        row = []
        for i, service in enumerate(services):
            service_name = getattr(service, f'name_{lang}')
            row.append(KeyboardButton(text=service_name))
            if (i + 1) % 2 == 0 or i == len(services) - 1:
                keyboard.append(row)
                row = []  
    keyboard.append([KeyboardButton(text=__('⬅️ Back',lang))])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    
async def get_all_service_category_keyboard(lang: str):
    async with models.async_session() as session:
        result = await session.execute(select(models.ServiceCategory).order_by(models.ServiceCategory.id))
        categories = result.scalars().all()  # Renamed 'products' to 'categories'

        keyboard = []
        row = []
        for i, category in enumerate(categories):
            category_name = getattr(category, f'name_{lang}', None)  # Select correct language
            if category_name:
                row.append(KeyboardButton(text=category_name))

            if (i + 1) % 2 == 0 or i == len(categories) - 1:
                keyboard.append(row)
                row = []  

    keyboard.append([KeyboardButton(text=__('⬅️ Back', lang))])  # Add Back button
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_all_service_category_keyboard_admin():
    async with models.async_session() as session:
        result = await session.execute(select(models.ServiceCategory))
        products = result.scalars().all()

        keyboard = []
        row = []
        for i, product in enumerate(products):
            row.append(KeyboardButton(text = product.name))
            if (i + 1) % 2 == 0 or i == len(products) - 1:
                keyboard.append(row)
                row = []  
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def create_new_order(full_name:str, phone_number:str, location:str, service_id:int, user_id:int):
    async with models.async_session() as session:
        new_order = models.Order(full_name=full_name,
                                 phone_number=phone_number,
                                 location=location,
                                 service_id=service_id,
                                 user_id=user_id
                                 )
        session.add(new_order)
        await session.commit()

async def get_service_by_name(name: str, lang: str):
    async with models.async_session() as session:
        name_column = getattr(models.Service, f'name_{lang}', None)
        if not name_column:
            return None 

        stmt = await session.execute(select(models.Service).where(name_column == name))
        service = stmt.scalar_one_or_none()  
        return service
    
async def get_all_order(telegram_id:int):
    async with models.async_session() as session:
        stmt = await session.execute(select(models.Order).join(models.User).options(selectinload(models.Order.service)).where(models.User.telegram_id==telegram_id))
        user_orders = stmt.scalars().all()
        return user_orders
    
async def change_language(telegram_id:int, lang:str):
    async with models.async_session() as session:
        stmt = await session.execute(update(models.User).where(models.User.telegram_id==telegram_id).values(language=lang))
        await session.commit()
        result = await session.execute(select(models.User).where(models.User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        return user
    
async def get_category_service_name(name: str, lang: str):
    async with models.async_session() as session:
        name_column = getattr(models.ServiceCategory, f'name_{lang}', None)
        if not name_column:
            return None  # Invalid language

        stmt = await session.execute(select(models.ServiceCategory).where(name_column == name))
        result = stmt.scalar_one_or_none()
        return result

# ✅ Create a new category in the specified language
async def create_category_service_name(name: str, lang: str):
    async with models.async_session() as session:
        column_name = f'name_{lang}'
        if not hasattr(models.ServiceCategory, column_name):
            return None  # Invalid language

        new_category_service = models.ServiceCategory(**{column_name: name})
        session.add(new_category_service)
        await session.commit()
        await session.refresh(new_category_service)  # Sync with DB
        return new_category_service

async def create_new_service(name:str, category_id:int, description:str):
    async with models.async_session() as session:
        new_service = models.Service(
            name=name,
            service_category_id=category_id,
            description=description
        )
        session.add(new_service)
        await session.commit()

async def get_all_order_admin():
    async with models.async_session() as session:
        stmt = await session.execute(select(models.Order).join(models.User).options(selectinload(models.Order.service)))
        user_orders = stmt.scalars().all()
        return user_orders
