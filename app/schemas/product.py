from pydantic import BaseModel

class ProductBase(BaseModel):
    brand: str | None = None
    model: str
    description: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True
