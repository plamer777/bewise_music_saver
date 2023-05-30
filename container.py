"""This file contains DAO and Service instances"""
from dao.user_dao import UserDao
from dao.file_dao import FileDao
from services.user_service import UserService
from services.file_service import FileService
# -------------------------------------------------------------------------

user_dao = UserDao()
user_service = UserService(user_dao)

file_dao = FileDao()
file_service = FileService(file_dao)
