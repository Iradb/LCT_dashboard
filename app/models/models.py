from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table,Float,JSON,ForeignKey,Text
from sqlalchemy.orm import relationship
from app.database.database import engine
from app.database.database import Base,Session

class Markers(Base):
    __tablename__ = 'Markers'
    # __metadata__ = metadata
    custom_id = Column(Integer, primary_key=True)
    custom_name = Column(String(50))
    lat = Column(Float)
    lon = Column(Float)
    def to_dict(self):
        return {
            'custom_name': self.custom_name,
            'custom_id': self.custom_id,
            'lat': self.lat,
            'lon': self.lon
        }
class TP(Base):
    __tablename__ = 'TP'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Adres_TP_Full = Column(String(200),nullable=True)
    Adres_TP = Column(String(80),nullable=True)
    Source_TP = Column(String(30),nullable=True)
    Balance_holder = Column(String(60),nullable=True)
    UNOM = Column(Integer,nullable=True)
    Number_TP = Column(String(50),nullable=True)
    Kind_TP = Column(String(10),nullable=True)
    id_ods = Column(Integer,ForeignKey("ODS.id_ods"),default=None,nullable=True)
    id_district = Column(Integer,ForeignKey("Admin_districts.id_district"),default=None,nullable=True)
    id_Municipal = Column(Integer,ForeignKey("Municipal_areas.id_area"),default=None,nullable=True)
    geoData = Column(JSON())
    geoData_full = Column(JSON())
    ods = relationship("ODS",backref="TP")
    district = relationship("Admin_districts",backref="TP")
    area = relationship("Municipal_areas",backref="TP")
class ODS(Base):
    __tablename__ = 'ODS'
    id_ods = Column(Integer, primary_key=True)
    Name = Column(String(100),nullable=True)
    Adres = Column(String(200),nullable=True)
    Phone_number = Column(String(30),nullable=True)
class Admin_districts(Base):
    __tablename__ = 'Admin_districts'
    id_district = Column(Integer, primary_key=True)
    name = Column(String(30),nullable=True)
    geocoords = Column(JSON(),default=None,nullable=True)
class Municipal_areas(Base):
    __tablename__ = 'Municipal_areas'
    id_area = Column(Integer, primary_key=True)
    id_district = Column(Integer,ForeignKey("Admin_districts.id_district"),default=None,nullable=True)
    name = Column(String(30),nullable=True)
    geocoords = Column(Text,default=None,nullable=True)
    district = relationship("Admin_districts",backref="Municipal_areas")
def add_db():
    session = Session()
    lat_1 = 59.936
    lon_1 = 30.339
    for i in range(0,4):
        marker = Markers(custom_name=str(i)+"DATA", lat=round(lat_1,3), lon=round(lon_1,3))
    # print(marker.custom_name, marker.lat, marker.lon)
        session.add(marker)
        lon_1 +=0.001
        lat_1 +=0.001
    session.commit()
    session.close()
        