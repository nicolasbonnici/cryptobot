from decouple import config
from sqlalchemy import create_engine

class Db:
    def __init__(self):
        self.instance = create_engine(config('DATABASE_URL'))