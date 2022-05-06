from sqlalchemy import (Column, Integer, MetaData,
                        String, Table, create_engine, ARRAY)

from databases import Database

import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(20)),
    Column('email', String(50))
)

database = Database(DATABASE_URL)
