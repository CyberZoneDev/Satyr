from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core import db_config

engine = create_engine('postgresql+psycopg2://{user}:{password}//:@{host}:{port}/{name}'.format(
    user=db_config['user'],
    password=db_config['password'],
    name=db_config['name'],
    host=db_config['host'],
    port=db_config['port']
), echo=False)

Base = declarative_base()
from .models import *

Base.metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()

__all__ = ['Session', 'engine']