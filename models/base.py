import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

class Base(DeclarativeBase):
    pass

engine = create_engine(url=os.getenv('DB_URL', ''), echo=True)
session_maker = sessionmaker(bind=engine)

def get_session():
    session = session_maker()
    try: 
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    