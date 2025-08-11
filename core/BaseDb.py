from typing import TypeVar, Generic, Type, Optional, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
import os
from asyncio import current_task
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

load_dotenv()
db_url = os.getenv("DB_URL")
engine = create_async_engine(url=db_url)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
ModelType = TypeVar("ModelType")


class BaseDAO(Generic[ModelType]):
    model: Type[ModelType]

    @classmethod
    async def get(cls, **filter_by) -> Optional[ModelType]:
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by) -> Optional[List[ModelType]]:
        """
        Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Список экземпляров модели.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, instance) -> Optional[ModelType]:
        """
        Добавляет уже созданный экземпляр модели в базу.

        Аргументы:
            instance: объект модели cls.model

        Возвращает:
            Добавленный экземпляр модели.
        """
        async with async_session_maker() as session:
            async with session.begin():
                session.add(instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return instance

    @classmethod
    async def update(cls, instance) -> Optional[ModelType]:
        """
        Асинхронно обновляет записи модели, удовлетворяющие фильтру, новыми значениями.

        Аргументы:
            filter_by: dict с условиями фильтрации (например, {"id": 1})
            values: dict с обновляемыми полями (например, {"verify": True})

        Возвращает:
            Количество обновленных записей.
        """
        async with async_session_maker() as session:
            async with session.begin():
                session.add(instance)
                try:
                    await session.commit()
                except SQLAlchemyError:
                    await session.rollback()
                    raise
                return instance

    @classmethod
    async def delete(cls, instance):
        """
        Асинхронно удаляет записи модели, удовлетворяющие фильтру.

        Аргументы:
            **filter_by: именованные параметры для фильтрации (например, id=1)

        Возвращает:
            Количество удалённых записей.
        """
        async with async_session_maker() as session:
            async with session.begin():
                await session.delete(instance)
                try:
                    await session.commit()
                except SQLAlchemyError:
                    await session.rollback()
                    raise
