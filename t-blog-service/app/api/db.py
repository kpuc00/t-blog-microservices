from sqlalchemy import (Column, Integer, MetaData,
                        String, Table, create_engine, ARRAY)
from databases import Database
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
metadata = MetaData()

blogs = Table(
    'blogs',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(20)),
    Column('description', String(250)),
    Column('authorId', Integer),
    Column('collaboratorsId', ARRAY(Integer))
)

database = Database(DATABASE_URL)
