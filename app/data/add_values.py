import sqlalchemy as sqlA
import os
import sys
sys.path.append(os.getcwd())
from app.models.models import TP,ODS,Admin_districts,Municipal_areas
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.schems.schem import Data_TP,Data_ODS,Data_Municipal_areas,Data_Admin_District
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
table = ["Полный адрес","Адрес ТП","Источник теплоснабжения","Балансодержатель","UNOM","ЦТП","geodata_center"]
# engine = sqlA.create_engine('sqlite:////app/myDatabase.db')
# engine = sqlA.create_engine('sqlite:///:memory:')
engine = sqlA.create_engine(f'mysql+pymysql://{os.getenv("LOG_DATABASE")}:{os.getenv("PASS")}@{os.getenv("IP_DATABASE")}:{os.getenv("PORT_DATABASE")}/{os.getenv("DATABASE")}')
Session  = sessionmaker(bind=engine)
# metadata = sqlA.MetaData()
Base = declarative_base()
Base.metadata.create_all(engine,tables=[ODS.__table__,Admin_districts.__table__,Municipal_areas.__table__,TP.__table__])
ctp = pd.read_csv("app/data/CTP.csv")
ods = pd.read_csv("app/data/ODS_INFO.csv")
adm_dist = pd.read_csv("administartion_district.csv")
municip = pd.read_csv("app/data/Municipal_area.csv")

def function_clear_data(string):
    try:
        start_index = string.find("[")
        end_index = string.rfind("]")
        if start_index != -1 and end_index != -1:
            substring = string[start_index + 1:end_index]
            substring = substring.split(",")
            integer_list = list(map(float, substring))
        else:
            print("Brackets not found")
    except:
        pass
        return None
    return integer_list
ctp["geodata_center"] = ctp["geodata_center"].apply(lambda x: function_clear_data(x))
# data = ctp[table]
def add_db_admin_municipal(data):
    list_mark = []
    session = Session()
    for _, row in data.iterrows():
        existing_row = session.query(Municipal_areas).filter_by(id_area=row['id']).first()
        if not existing_row:
            try:
                marker = Data_Municipal_areas(id_area=row["id"],
                            name=row["Муницип.Район"]
                            )
                list_mark.append(marker)    
            except Exception as e:
                print(e)
                continue
    session.bulk_insert_mappings(Municipal_areas, list_mark)
    session.commit()
    session.close()
def add_db_admin_district(data):
    list_mark = []
    session = Session()
    for _, row in data.iterrows():
        try:
            existing_row = session.query(Admin_districts).filter_by(id_district=row['id']).first()
            if not existing_row:
                marker = Data_Admin_District(id_district=row["id"],
                            name=row["Админ округ (ТП)"]
                            )
                list_mark.append(marker)    
        except Exception as e:
            print(e)
            continue
    session.bulk_insert_mappings(Admin_districts, list_mark)
    session.commit()
    session.close()
def add_db_ODS(data):
    list_mark = []
    session = Session()
    for _, row in data.iterrows():
        try:
            existing_row = session.query(ODS).filter_by(id_ods=row["ID ODS"]).first()
            if not existing_row:
                marker = Data_ODS(id_ods=int(row["ID ODS"]),
                            Name=row["NAME"],
                            Adres=row["ADDRESS"],
                            Phone_number=row["PHONE_NUMBER"])
                list_mark.append(marker)    
        except Exception as e:
            print(e)
            continue
    session.bulk_insert_mappings(ODS, list_mark)
    session.commit()
    session.close()
def add_db_CTP(data):
    list_mark = []
    
    for _, row in data.iterrows():
        try:
            marker = Data_TP(
                Adres_TP_Full=row['Полный адрес'],
                Adres_TP=row['Адрес ТП'],
                Source_TP=row['Источник теплоснабжения'],
                Balance_holder=row['Балансодержатель'],
                UNOM=row['UNOM'],
                Number_TP=row['ЦТП'],
                geoData_full=row['geodata_center'],
                Kind_TP=row["Вид ТП"],
                id_ods=row["ID ODS"],
                id_district=row["id_administration"],
                id_Municipal=row["id_Municipal"],
            )
            list_mark.append(marker)    
        except Exception as e:
            print(e)
            continue
    session = Session()
    session.bulk_insert_mappings(TP, list_mark)
    # session.add(marker)
    session.commit()
    session.close()
# add_db_CTP()
add_db_admin_municipal(municip)
add_db_admin_district(adm_dist)
add_db_ODS(ods)
add_db_CTP(ctp)
