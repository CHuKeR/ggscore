from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.config import config

engine = create_engine(config.DB_URI, echo=True)

session = scoped_session(sessionmaker(bind=engine))
