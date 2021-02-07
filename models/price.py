from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, DECIMAL
import uuid
import datetime

db = create_engine(config('DATABASE_URL'))
base = declarative_base()


class Price(base):
    __tablename__ = 'price'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    pair = Column(String, nullable=False)
    curr = Column(DECIMAL(16, 8), nullable=False)
    lowest = Column(DECIMAL(16, 8), nullable=False)
    highest = Column(DECIMAL(16, 8), nullable=False)
    created = Column(DateTime, default=datetime.datetime.utcnow)


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)