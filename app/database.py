# app/database.py
import os
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
metadata = MetaData()

urls = Table(
    "urls",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String, nullable=False),
    Column("status", String, nullable=False),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
