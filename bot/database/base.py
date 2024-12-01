from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from typing import AsyncGenerator

from config import load_config
from bot.database.models import Base  # Импортируйте Base, который включает все ваши модели

# Создаем движок базы данных
config = load_config()
engine = create_async_engine(config.db.database, echo=True)

# Создаем фабрику сессий
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Функция для получения сессии
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session 

# Функция для создания всех таблиц
async def create_tables():
    async with engine.begin() as conn:
        # Создаем все таблицы, определенные в Base
        await conn.run_sync(Base.metadata.create_all) 