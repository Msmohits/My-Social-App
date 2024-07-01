from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2

SQLITE_DATABASE_URL = "postgresql+psycopg2://vryno:vryno123@localhost/vryno"

engine = create_engine(SQLITE_DATABASE_URL, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
