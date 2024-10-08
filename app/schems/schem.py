from datetime import datetime
from typing import Tuple,Type, TypeVar,Optional
from pydantic import BaseModel,Field,root_validator,model_validator
from app.database.database import Base
import pandas as pd

T = TypeVar('T', bound=BaseModel)


"""
Типизированные схемы для работы с БД и запросов к ним
"""
# Utility function to convert SQLAlchemy objects to Pydantic models.
def to_pydantic(db_object: Base, pydantic_model: Type[T]) -> T:
    return pydantic_model(**db_object.__dict__)

class Object_take(BaseModel):
    name:str
    lat:float
    lon:float

class Data_TP(BaseModel):
    Adres_TP_Full:Optional[str] = Field(default=None, allow_nan=True)
    Adres_TP:Optional[str] = Field(default=None, allow_nan=True)
    Source_TP:Optional[str] = Field(default=None, allow_nan=True)
    Balance_holder:Optional[str] = Field(default=None, allow_nan=True)
    UNOM:Optional[int] = Field(default=None, allow_nan=True)
    Number_TP:Optional[str] = Field(default=None, allow_nan=True)
    Kind_TP:Optional[str] = Field(default=None, allow_nan=True)
    id_ods:Optional[int] = Field(default=None, allow_nan=True)
    id_district:Optional[int] = Field(default=None, allow_nan=True)
    id_Municipal:Optional[int] = Field(default=None, allow_nan=True)
    geoData_full:Optional[list] = Field(default=None, allow_nan=True)

class Data_ODS(BaseModel):
    id_ods:int
    Name:str
    Adres:str
    Phone_number:str
class Data_Municipal_areas(BaseModel):
    id_area:int
    name:str
    id_district:int
    geocoords:Optional[str]
class Data_Admin_District(BaseModel):
    id_district:int
    name:str
