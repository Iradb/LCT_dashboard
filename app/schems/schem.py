from datetime import datetime
from typing import Tuple,Type, TypeVar
from pydantic import BaseModel
from app.database.database import Base


T = TypeVar('T', bound=BaseModel)



# Utility function to convert SQLAlchemy objects to Pydantic models.
def to_pydantic(db_object: Base, pydantic_model: Type[T]) -> T:
    return pydantic_model(**db_object.__dict__)

class Object_take(BaseModel):
    name:str
    lat:float
    lon:float
