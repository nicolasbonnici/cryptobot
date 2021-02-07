from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import price


def run(symbol, msg):
    print(msg['b'])

    db = create_engine(config('DATABASE_URL'))

    Session = sessionmaker(db)
    session = Session()

    newPrice = price.Price(pair=symbol, curr=msg['b'], lowest=msg['l'], highest=msg['h'])
    session.add(newPrice)
    session.commit()