from os import getenv
import asyncio

from sqlalchemy import String, Integer, DateTime, Boolean, Column, ForeignKey, func, BigInteger
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine

DB_USER = getenv('DB_USER','postgres')
DB_NAME = getenv('DB_NAME','service_db')
DB_PASSWORD = getenv('DB_PASSWORD','admin123')
DB_HOST = getenv('DB_HOST','localhost')
DB_PORT =int(getenv('DB_PORT',5432))

engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    created_time = Column(DateTime,default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    language = Column(String, nullable=False)

    #relationship
    order = relationship('Order', back_populates='user')


class ServiceCategory(Base):
    __tablename__ = 'service_category'

    id = Column(Integer, primary_key=True)
    name_uz = Column(String, nullable=True, unique=True)
    name_ru = Column(String)
    name_en = Column(String)

    #relationship
    service = relationship('Service', back_populates='service_category')


class Service(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    name_uz = Column(String, nullable=True, unique=True)
    name_ru = Column(String)
    name_en = Column(String)
    description_uz = Column(String, nullable=True)
    description_ru = Column(String, nullable=True)
    description_en = Column(String, nullable=True)
    calculate = Column(Boolean, default=False)
    price = Column(String, default=None)
    service_category_id = Column(ForeignKey('service_category.id', ondelete='CASCADE'))

    #relationships
    order = relationship('Order', back_populates='service')
    service_category = relationship('ServiceCategory', back_populates='service')

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'))
    full_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=False)
    location = Column(String, nullable=True)
    service_id = Column(ForeignKey('service.id', ondelete='CASCADE'))

    #relationship
    service = relationship('Service', back_populates='order')
    user = relationship('User', back_populates='order')