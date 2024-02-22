# model.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from config import SQLALCHEMY_DATABASE_URL

Base = declarative_base()

class BoxSize(PyEnum):
    big = "big"
    medium = "medium"
    small = "small"

class Tenant(Base):
    __tablename__ = "tenants"
    tenant_id = Column(Integer, primary_key=True, index=True)
    tenant_name = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    users = relationship("User", back_populates="tenant")
    products = relationship("Product", back_populates="tenant")

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tenant = relationship("Tenant", back_populates="users")
    roles = relationship("Role", secondary='user_roles', back_populates="users")

class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)
    users = relationship("User", secondary='user_roles', back_populates="roles")

user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('role_id', ForeignKey('roles.role_id'), primary_key=True)
)

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'))
    product_name = Column(String, index=True)
    box_size = Column(Enum(BoxSize))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tenant = relationship("Tenant", back_populates="products")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
