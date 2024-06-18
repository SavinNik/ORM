import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale, drop_tables
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
login = config["SETTINGS"]["login"]
password = config["SETTINGS"]["password"]
db_name = config["SETTINGS"]["db_name"]

DSN = f'postgresql://{login}:{password}@localhost:5432/{db_name}'
engine = sqlalchemy.create_engine(DSN)

drop_tables(engine)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', encoding="utf-8") as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


def get_info(publisher_info):
    if publisher_info.isdigit():
        for i in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(
                Shop).join(Sale).filter(Publisher.id == publisher_info).all():
            print(f'{i[0]} | {i[1]} | {i[2]} | {i[3]}')
    else:
        for i in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(
                Shop).join(Sale).filter(Publisher.name.like(f'%{publisher_info}%')).all():
            print(f'{i[0]} | {i[1]} | {i[2]} | {i[3]}')


session.close()

if __name__ == "__main__":
    user_input = input("Введите имя или id издателя:\n")
    get_info(user_input)
