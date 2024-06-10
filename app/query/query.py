from app.database.database import Session
from app.models.models import Markers,TP,ODS,Admin_districts,Municipal_areas

def take_group():
    session = Session()
    query = session.query(Municipal_areas.id_area,Municipal_areas.name).all()
    query = [{"id":str(row[0]),'Муницип.Район': row[1]} for row in query]
    session.close()
    return query

def take_data_TCP(id):
    session = Session()
    query = session.query(TP.id,TP.Adres_TP_Full,TP.Kind_TP,TP.Number_TP).all()
    query = [{"id":str(row[0]),'Адрес': row[1],'Вид ТП': row[2],'UNOM': row[1]} for row in query]
    session.close()
    return query