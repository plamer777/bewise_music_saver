"""This file contains utility functions"""
import os
from typing import BinaryIO
from uuid import uuid4
from pydub import AudioSegment
from fastapi.exceptions import HTTPException
from constants import MEDIA_PATH, BASE_URL
from dao import LocalSession
from dao.models import File
# ------------------------------------------------------------------------


async def get_db() -> LocalSession:
    """This function serves to get a database session"""
    async with LocalSession() as db:
        return db


def save_wav_to_mp3_file(file_obj: BinaryIO) -> str:
    """The function serves to converse and save provided wav file
    :param file_obj: opened wav file to convert and save
    :return: a string representing url to download the file
    """
    if not os.path.exists(MEDIA_PATH):
        os.mkdir(MEDIA_PATH)

    try:
        file_uuid = uuid4().hex
        file_path = os.path.join(MEDIA_PATH, file_uuid + '.mp3')
        AudioSegment.from_file(file_obj).export(file_path)
        return file_uuid

    except Exception as e:
        raise HTTPException(
            400, {'error': f'Could not save file, the error: {e}'})


def create_url(model: File) -> str:
    """This function serves to prepare url to download saved files
    :param model: a File model with necessary data
    :return: a prepared url
    """
    file_url = f'{BASE_URL}id={model.id}&user={model.user_id}'
    return file_url


def create_file_path(file: File) -> str:
    """This function serves to prepare path fo file to save
    :param file: a File model with necessary data
    :return: a string representing prepared path
    """
    file_path = os.path.join(MEDIA_PATH, file.uuid + '.mp3')
    return file_path

