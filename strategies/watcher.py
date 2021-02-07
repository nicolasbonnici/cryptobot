from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import price

db = create_engine(config('DATABASE_URL'))

Session = sessionmaker(db)
session = Session()


def run(newPrice: price.Price):
    print('Symbol: ', newPrice.pair, 'Price: ', newPrice.curr)

    # Persist price
    session.add(newPrice)
    session.commit()