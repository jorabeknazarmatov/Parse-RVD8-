from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base


class Catalog(Base):
    __tablename__ = "catalogs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=True)
    link = Column(String(255), index=True, nullable=True)
    
    

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    catalog_id = Column(Integer, index=True)
    brand = Column(String(255), index=True, nullable=True)
    model = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    link = Column(String(255), index=True, nullable=True)
    
    
