"""This file contains model classes to get access to the database"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dao import Base
# -------------------------------------------------------------------------


class File(Base):
    """This class represents a file spreadsheet"""
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(255), unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')


class User(Base):
    """This class represents a user spreadsheet"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), unique=True)
    uuid = Column(String(255), unique=True)
