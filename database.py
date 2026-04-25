from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Tell python where is database
DATABASE_URL='postgresql://postgres:root@localhost:5432/fastapi'

# create DB connection using engine
engine = create_engine(DATABASE_URL)

# DB Operations with sessionLocal
sessionLocal = sessionmaker(bind=engine)

# a base to create table.
Base = declarative_base()
