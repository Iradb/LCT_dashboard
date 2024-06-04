import sqlalchemy as sqlA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# engine = sqlA.create_engine('sqlite:////app/myDatabase.db')
engine = sqlA.create_engine('sqlite:///:memory:')
Session  = sessionmaker(bind=engine)
# metadata = sqlA.MetaData()
Base = declarative_base()
session = Session()
