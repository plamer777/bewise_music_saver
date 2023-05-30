"""This file contains schemas works as validators and serializers"""
from uuid import uuid4
from pydantic import BaseModel
from pydantic.class_validators import root_validator
# -------------------------------------------------------------------------


class UserBaseSchema(BaseModel):
    """This class contains a base fields to be inherited by another classes"""
    id: int | None = None
    uuid: str

    class Config:
        orm_mode = True


class UserRegisterSchema(UserBaseSchema):
    """The class serves as serializer during registration process"""
    username: str

    @root_validator(pre=True)
    def create_uuid(cls, values: dict) -> dict:
        values['uuid'] = uuid4().hex
        return values


class UserSchema(UserBaseSchema):
    """This class used as serializer in all processes except registration"""
    id: int
    uuid: str


class FileSchema(BaseModel):
    """This class serves as serializer during save file process"""
    uuid: str
    user_id: int


class DownloadFileSchema(BaseModel):
    """This class serves as serializer during download file process"""
    id: int
    user_id: int
