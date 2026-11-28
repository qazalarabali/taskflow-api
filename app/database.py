
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# CONFIGURATION
load_dotenv()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    database=os.getenv("POSTGRES_DB")
)


# DATABASE ENGINE
engine = create_engine(database_url)


# SESSION
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# BASE MODEL
class Base(DeclarativeBase):
    pass

# SESSION DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()