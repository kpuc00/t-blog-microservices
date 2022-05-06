from sqlalchemy import (Column, Integer, MetaData,
                        String, Table, create_engine, DATETIME)
from databases import Database
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
metadata = MetaData()

comments = Table(
    'comments',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('content', String(1000), nullable=False),
    Column('userId', Integer, nullable=False),
    # Column('created', DATETIME, nullable=False),
    # Column('modified', DATETIME),
    Column('articleId', Integer, nullable=False)

)

database = Database(DATABASE_URL)
