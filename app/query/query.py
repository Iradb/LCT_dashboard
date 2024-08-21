from app.database.database import Session
from app.models.models import Markers,TP,ODS,Admin_districts,Municipal_areas
from shapely.wkt import loads
from shapely.geometry import MultiPolygon,Polygon

def take_data_TCP(id:int)->dict:
    """
    Запрос на получение информации о районе
    """
    session = Session()
    query = session.query(TP, ODS).outerjoin(ODS, TP.id_ods == ODS.id_ods).filter(TP.id == id).first()
    if query:
        row_TP = query[0]
        row_ODS = query[1]
        print(row_ODS)
        query_complete = [{"id": str(row_TP.id),
                  'Адрес':row_TP.Adres_TP_Full if row_TP.Adres_TP_Full != None else None,
                  'Вид ТП': row_TP.Kind_TP if row_TP.Kind_TP != None else None,
                  'UNOM': row_TP.UNOM if row_TP.UNOM!= None else None,
                  "ODS_name": row_ODS.Name if row_ODS != None else None,
                  "ODS_adrs": row_ODS.Adres if row_ODS != None else None,
                  "ODS_number": row_ODS.Phone_number if row_ODS != None else None}]
    session.close()
    return query_complete
def Take_geoodata_Municipal()->dict:
    """
    Запрос на получение информации о районах (id,наименования,координат)
    """
    session = Session()
    query = session.query(Municipal_areas.id_area,Municipal_areas.name,Municipal_areas.geocoords).all()
    query_complete = [{"id":str(row[0]),'Муницип.Район': row[1],'geocoords': Polygon(loads(row[2]).geoms[0]) if isinstance(loads(row[2]), MultiPolygon) else loads(row[2])} for row in query]
    session.close()
    return query_complete
