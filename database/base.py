from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import setting

Base = declarative_base()

engine = create_engine(setting.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
