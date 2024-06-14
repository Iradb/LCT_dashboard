from app.database.database import Session
from app.models.models import Markers,TP,ODS,Admin_districts,Municipal_areas
from shapely.wkt import loads
from shapely.geometry import MultiPolygon,Polygon
def take_group():
    session = Session()
    query = session.query(Municipal_areas.id_area,Municipal_areas.name).all()
    query = [{"id":str(row[0]),'Муницип.Район': row[1]} for row in query]
    session.close()
    return query

def take_data_TCP(id):
    session = Session()
    # query = session.query(TP.id,TP.Adres_TP_Full,TP.Kind_TP,TP.Number_TP,TP.ods).where(TP.id == id).first()
    query = session.query(TP, ODS).outerjoin(ODS, TP.id_ods == ODS.id_ods).filter(TP.id == id).first()
    if query:
        row_TP = query[0]
        row_ODS = query[1]
        # print(row_TP.id, row_ODS.Name, row_ODS.Adres, row_ODS.Phone_number)
        query = [{"id": str(row_TP.id),
                  'Адрес':row_TP.Adres_TP_Full if row_TP.Adres_TP_Full != None else None,
                  'Вид ТП': row_TP.Kind_TP if row_TP.Kind_TP != None else None,
                  'UNOM': row_TP.UNOM if row_TP.UNOM!= None else None,
                  "ODS_name": row_ODS.Name if row_ODS.Name != None else None,
                  "ODS_adrs": row_ODS.Adres if row_ODS.Adres != None else None,
                  "ODS_number": row_ODS.Phone_number if row_ODS.Phone_number != None else None}]
        # print(row_TP.id,row_ODS.Name,row_ODS.Adres,row_ODS.Phone_number)
    # query = [{"id":str(row_TP.id),'Адрес': row_TP.Adres_TP_Full,'Вид ТП': row_TP.Kind_TP,'UNOM': row_TP.UNOM,
    #           "ODS_name":row_ODS.Name,"ODS_adrs":row_ODS.Adres,"ODS_number":row_ODS.Phone_number} for row_TP,row_ODS in query]
    session.close()
    return query
def Take_geoodata_Municipal():
    session = Session()
    query = session.query(Municipal_areas.id_area,Municipal_areas.name,Municipal_areas.geocoords).all()
    # query_ret = []
    # for row in query:
    #     rows = loads(row[2])
    #     if isinstance(rows, MultiPolygon):
    #         print("The object is a MultiPolygon")
    query = [{"id":str(row[0]),'Муницип.Район': row[1],'geocoords': Polygon(loads(row[2]).geoms[0]) if isinstance(loads(row[2]), MultiPolygon) else loads(row[2])} for row in query]
    session.close()
    return query
