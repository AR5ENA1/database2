#psycopg2
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, Base
import json


def add_data(session, file):
    with open(file, 'r') as fd:
        data = json.load(fd)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))


def print_publisher(session):
    # try:
    #     id_publisher = int(input("Пожалуйста введите ID создателя, которого необходимо вывести: "))
    # except ValueError:
    #     print('Неврное значение, это должно быть целое число')
    # else:
    id_publisher = int(input("Пожалуйста введите ID создателя, которого необходимо вывести: "))
    if id_publisher not in range(1,5):
        print("Некорректны ID, значение должно быть от 1 до 4")
    else:
        subq = session.query(Publisher).filter(Publisher.id == id_publisher).subquery()
        for i in session.query(Stock, Book, Shop, Sale).join(Book).join(Shop).join(Sale).join(
                subq, Book.id_publisher == subq.c.id):
            print(f"{i.Book.title} | {i.Shop.name} | {i.Stock.count} | {i.Sale.count}")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    DSN = 'postgresql://postgres:</////>@localhost:5432/database2'
    engine = sq.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    add_data(session, 'tests_data.json')
    session.commit()

    print_publisher(session)

    session.close()


