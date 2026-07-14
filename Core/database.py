from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL=settings.database_url

engine=create_engine(SQLALCHEMY_DATABASE_URL)

session=sessionmaker(autocommit=False,autoflush=False,bind=engine)

base=declarative_base()

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()