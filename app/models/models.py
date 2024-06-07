from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table,Float
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
        