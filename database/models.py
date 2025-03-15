from os import getenv
import asyncio

from sqlalchemy import String, Integer, DateTime, Boolean, Column, ForeignKey, func, BigInteger
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine

DB_USER = getenv('DB_USER')
DB_NAME = getenv('DB_NAME')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT',5432)

engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

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
    name = Column(String, nullable=False, unique=True)

    #relationship
    service = relationship('Service', back_populates='service_category')


class Service(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
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


