"""This file contains services with business logic"""
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dao.models import User
from dao.user_dao import UserDao
from services.schemas import UserRegisterSchema, UserSchema
# --------------------------------------------------------------------------


class UserService:
    """The UserService class provides an interface to process user requests"""
    def __init__(self, dao: UserDao) -> None:
        """Initialize the service
        :param dao: an instance of UserDao class
        """
        self._dao = dao

    async def register(
            self, db: AsyncSession, user: UserRegisterSchema) -> User:
        """This method serves to register a new user
        :param db: an instance of the AsyncSession
        :param user: an instance of UserRegisterSchema with registration data
        :return: a User model or None if there was an error during registration
        """
        if await self._dao.get_by_username(db, user.username):
            raise HTTPException(
                400, {'error': 'The user with this username is already exists'})

        new_user = await self._dao.add(db, user)
        if not new_user:
            raise HTTPException(
                400, {'error': 'Failed to register user'})

        return new_user

    async def get_by_uuid_and_id(
            self, db: AsyncSession, user: UserSchema) -> User:
        """This method serves to get user by uuid and id
        :param db: an instance of the AsyncSession
        :param user: an instance of UserSchema with necessary data
        :return: a User model
        """
        found_user = await self._dao.get_by_uuid_and_id(db, user)
        if not found_user:
            raise HTTPException(
                404, {'error': 'User not found, please check your id and uuid'})
        return found_user

    def __repr__(self) -> str:
        """Representation of the class instance"""
        return f'UserService({self._dao})'
