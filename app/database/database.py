import sqlalchemy as sqlA
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# engine = sqlA.create_engine('sqlite:////app/myDatabase.db')
# engine = sqlA.create_engine('sqlite:///:memory:')
engine = sqlA.create_engine(f'mysql+pymysql://{os.getenv("LOG_DATABASE")}:{os.getenv("PASS")}@{os.getenv("IP_DATABASE")}:{os.getenv("PORT_DATABASE")}/{os.getenv("DATABASE")}')
Session  = sessionmaker(bind=engine)
# metadata = sqlA.MetaData()
Base = declarative_base()
