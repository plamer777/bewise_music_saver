"""This file contains DAO objects to work with the database"""
from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from dao import Base
from dao.models import User
from services.schemas import UserRegisterSchema, UserSchema
# -------------------------------------------------------------------------


class UserDao:
    """The UserDao class provides access to the database"""
    def __init__(self, model: Base = User) -> None:
        """Initialize the TaskDao class
        :param model: a class inherited from Base
        """
        self._model = model

    async def add(
            self, db: AsyncSession, user: UserRegisterSchema) -> User | None:
        """This method adds a new user to the database
        :param db: an instance of the AsyncSession
        :param user: an instance of UserRegisterSchema with data to add
        :return: a User model or None if there was IntegrityError during the
        operation
        """
        try:
            new_user = self._model(**user.dict(exclude={'id'}))
            db.add(new_user)
            await db.commit()
            return new_user
        except IntegrityError as e:
            await db.rollback()
            print(f'An error occurred while adding the record: {e}')
            return None

    async def update(
            self, db: AsyncSession, user: UserSchema) -> User | None:
        try:
            await db.execute(update(self._model).where(
                self._model.id == user.id, self._model.uuid == user.uuid
            ).values(**user.dict()))
        except Exception as e:
            print(f'An error occurred while updating the record: {e}')
            return None

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:

        found_user = await db.get(self._model, user_id)
        return found_user

    async def get_by_username(
            self, db: AsyncSession, username: str) -> User | None:

        found_user = await db.execute(select(self._model).where(
            self._model.username == username))

        return found_user.scalar()

    async def get_by_uuid_and_id(
            self, db: AsyncSession, user: UserSchema) -> User | None:

        found_user = await db.execute(select(self._model).where(
            self._model.uuid == user.uuid, self._model.id == user.id))

        return found_user.scalar()

    def __repr__(self) -> str:
        """Representation of the UserDao class"""
        return f'UserDao({self._model})'
