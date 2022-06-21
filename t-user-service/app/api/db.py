from sqlalchemy import (Column, Integer, MetaData,
                        String, Boolean, Table, create_engine)
from databases import Database
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(20), nullable=False),
    Column('first_name', String(40), nullable=False),
    Column('last_name', String(40), nullable=False),
    Column('email', String(50), nullable=False),
    Column('password', String(130), nullable=False),
    Column('disabled', Boolean)
)

database = Database(DATABASE_URL)
