from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine("postgresql://developer:qS*7Pjs3v0kw@db.g97.io:5432/data_analyst", 
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
