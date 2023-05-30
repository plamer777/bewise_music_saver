"""This is a main file to start the application"""
from fastapi import FastAPI, Depends, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from constants import API_VERSION, API_TITLE, API_DESCRIPTION
from container import user_service, file_service
from services.schemas import UserSchema, UserRegisterSchema, FileSchema, \
    DownloadFileSchema
from utils import get_db, save_wav_to_mp3_file, create_file_path
# --------------------------------------------------------------------------

api = FastAPI(
    version=API_VERSION, title=API_TITLE, description=API_DESCRIPTION)


@api.get('/', status_code=301)
async def index() -> RedirectResponse:
    """This view serves to redirect requests from root route to /docs
    :return: a RedirectResponse object
    """
    return RedirectResponse('/docs', status_code=301)


@api.post('/users/register', status_code=201)
async def register_page(
        user_data: UserRegisterSchema, db: AsyncSession = Depends(get_db)
) -> UserSchema:
    """This view registers new users
    :param user_data: a UserRegisterSchema class
    :param db: an instance of AsyncSession
    :return: json with user id and uuid
    """
    added_user = await user_service.register(db, user_data)

    return added_user


@api.post('/files/upload', status_code=201)
async def upload_file(
        user_id: int, uuid: str, file: UploadFile,
        db: AsyncSession = Depends(get_db)
) -> str:
    """This view serves to upload new music files (.wav format)
    :param uuid: a string representing unique user token
    :param user_id: an integer representing user id
    :param file: an UploadFile object
    :param db: an instance of AsyncSession
    :return: url to download the file
    """
    file_uuid = save_wav_to_mp3_file(file.file)
    requested_user = UserSchema(id=user_id, uuid=uuid)
    found_user = await user_service.get_by_uuid_and_id(db, requested_user)
    file_schema = FileSchema(uuid=file_uuid, user_id=found_user.id)
    file_url = await file_service.save(db, file_schema)

    return file_url


@api.get('/record')
async def download_file(
        id: int, user: int, db: AsyncSession = Depends(get_db)) -> FileResponse:
    """This view serves to download previously uploaded files in .mp3 format
    :param id: an integer representing a file id
    :param user: an integer representing user id
    :param db: an instance of AsyncSession
    :return: json with user id and uuid
    """
    requested_file = DownloadFileSchema(id=id, user_id=user)
    found_file = await file_service.get_by_id_and_user(db, requested_file)
    file_path = create_file_path(found_file)
    return FileResponse(file_path)
