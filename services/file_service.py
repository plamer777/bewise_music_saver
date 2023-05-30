"""This file contains services with business logic"""
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dao.file_dao import FileDao
from dao.models import File
from services.schemas import FileSchema, DownloadFileSchema
from utils import create_url
# --------------------------------------------------------------------------


class FileService:
    """The FileService class provides an interface to process user requests"""
    def __init__(self, dao: FileDao) -> None:
        """Initialize the service
        :param dao: an instance of FileDao class
        """
        self._dao = dao

    async def save(
            self, db: AsyncSession, file: FileSchema) -> str:
        """This method serves to check and add new file to the database
        :param db: an instance of the AsyncSession
        :param file: an instance of FileSchema with necessary data
        :return: a string representing url to download the file
        """
        file_result = await self._dao.add(db, file)
        if type(file_result) is str:
            raise HTTPException(
                400, {'error': file_result})
        file_url = create_url(file_result)
        return file_url

    async def get_by_id_and_user(
            self, db: AsyncSession, file: DownloadFileSchema) -> File:
        """This method serves to get a file model by its id and user
        :param db: an instance of the AsyncSession
        :param file: an instance of DownloadFileSchema
        :return: a File model
        """
        found_file = await self._dao.get_by_id_and_user(db, file)
        if not found_file:
            raise HTTPException(
                404, {'error': 'File not found, please check file and user id'})
        return found_file

    def __repr__(self) -> str:
        """Representation of the class instance"""
        return f'FileService({self._dao})'
