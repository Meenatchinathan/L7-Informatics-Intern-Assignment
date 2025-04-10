from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///expenses.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_db_session():
    return Session()