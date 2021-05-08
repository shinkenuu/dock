from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from desafio.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_recycle=3600)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class LocalSession:
    def __init__(self, session=None):
        self.ours_to_close = not bool(session)
        self.db = session if session else Session()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        if self.ours_to_close:
            self.db.close()
