from sqlalchemy.orm import sessionmaker
from .db_setup import engine

SessionLocal = sessionmaker(bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()