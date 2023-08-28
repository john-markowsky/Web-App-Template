# database.py
from sqlalchemy import inspect, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import datetime, os

# Choose the database URL based on the environment variable
if os.environ.get("ENV") == "TEST":
    DATABASE_URL = "sqlite:///:memory:"
else:
    DATABASE_URL = "sqlite:///./{BRAND_NAME}.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subject = Column(String)
    issuer = Column(String)
    valid_from = Column(String, default=datetime.date.today().strftime('%Y-%m-%d'))
    valid_until = Column(String, default=datetime.date.today().strftime('%Y-%m-%d'))
    status = Column(String)

    def set_valid_from(self, date):
        if isinstance(date, datetime.date):
            self.valid_from = date.strftime('%Y-%m-%d')
        else:
            self.valid_from = date

    def set_valid_until(self, date):
        if isinstance(date, datetime.date):
            self.valid_until = date.strftime('%Y-%m-%d')
        else:
            self.valid_until = date

class ActiveHost(Base):
    __tablename__ = "active_hosts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    ip_address = Column(String)