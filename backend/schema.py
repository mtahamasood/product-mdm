# schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from model import BoxSize

class TenantBase(BaseModel):
    tenant_name: str

class TenantCreate(TenantBase):
    pass

class TenantInDB(TenantBase):
    tenant_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    tenant_id: int
    email: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    role_name: str

class RoleCreate(RoleBase):
    pass

class RoleInDB(RoleBase):
    role_id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    tenant_id: int
    product_name: str
    box_size: BoxSize

class ProductCreate(ProductBase):
    pass

class ProductInDB(ProductBase):
    product_id: int
    created_at: datetime

    class Config:
        orm_mode = True
