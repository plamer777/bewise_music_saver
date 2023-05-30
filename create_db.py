"""This file serves to create database tables"""
from asyncio import run
from constants import CLEAR_DB
from dao import Base, engine
from dao.models import User, File
# -------------------------------------------------------------------------


async def create_tables():
    """The function creates tables"""
    async with engine.begin() as conn:
        if CLEAR_DB:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


run(create_tables())
