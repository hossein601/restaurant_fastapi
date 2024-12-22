from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config import setting
Base = declarative_base()
engine = create_engine(setting.DATABASE_URL, echo=True)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        Session.remove()

def init_db():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
