from sqlalchemy import (Column, Integer, MetaData,
                        String, Table, create_engine, DATETIME)
from databases import Database
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
metadata = MetaData()

articles = Table(
    'articles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(20), nullable=False),
    Column('content', String(1000)),
    Column('authorId', Integer, nullable=False),
    # Column('created', DATETIME, nullable=False),
    # Column('modified', DATETIME),
    Column('blogId', Integer, nullable=False)

)

database = Database(DATABASE_URL)
