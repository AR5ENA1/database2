import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from models import Publisher, Book, Shop, Stock, Sale, create_tables, add_data, print_publisher


if __name__ == '__main__':
    DSN = 'postgresql://postgres:**********@localhost:5432/database2'
    engine = sq.create_engine(DSN)
    # create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    add_data(session, 'tests_data.json')
    session.commit()

    print_publisher(session)

    session.close()


