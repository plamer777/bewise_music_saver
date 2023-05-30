"""This file contains DAO objects to work with the database"""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from dao import Base
from dao.models import File
from services.schemas import FileSchema, DownloadFileSchema
# -------------------------------------------------------------------------


class FileDao:
    """The FileDao class provides access to the database"""
    def __init__(self, model: Base = File) -> None:
        """Initialize the FileDao class
        :param model: a class inherited from Base
        """
        self._model = model

    async def add(
            self, db: AsyncSession, file: FileSchema) -> File | str:
        """This method adds a new record to the database
        :param db: an instance of the AsyncSession
        :param file: an instance of FileSchema with data to add
        :return: a File model or None if there was IntegrityError during the
        operation
        """
        try:
            new_file = self._model(**file.dict(exclude={'id'}))
            db.add(new_file)
            await db.commit()
            return new_file
        except IntegrityError as e:
            await db.rollback()
            return (f'An error occurred while adding the record to the '
                    f'database: {e}')

    async def get_by_id_and_user(
            self, db: AsyncSession, file: DownloadFileSchema) -> File | None:
        """This method returns a File model found by its id and user
        :param db: an instance of the AsyncSession
        :param file: an instance of DownloadFileSchema
        :return: a File model or None if file is not found
        """
        found_file = await db.execute(select(self._model).where(
            self._model.id == file.id, self._model.user_id == file.user_id))

        return found_file.scalar()
