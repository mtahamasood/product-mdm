# router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schema
from model import SessionLocal 
from schema import UserInDB
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token ,ACCESS_TOKEN_EXPIRE_MINUTES , role_required ,get_current_user_with_roles
from datetime import timedelta


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Tenant routes
@router.post("/tenants/", response_model=schema.TenantInDB)
def create_tenant(tenant: schema.TenantCreate, db: Session = Depends(get_db)):
    return crud.create_tenant(db=db, tenant=tenant)

@router.get("/tenants/", response_model=List[schema.TenantInDB])
def read_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tenants(db, skip=skip, limit=limit)

@router.put("/tenants/{tenant_id}", response_model=schema.TenantInDB)
def update_tenant(tenant_id: int, tenant: schema.TenantCreate, db: Session = Depends(get_db)):
    return crud.update_tenant(db=db, tenant_id=tenant_id, tenant_update=tenant)

@router.delete("/tenants/{tenant_id}")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    crud.delete_tenant(db=db, tenant_id=tenant_id)
    return {"detail": "Tenant deleted successfully"}

# User routes
@router.post("/users/", response_model=schema.UserInDB)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schema.UserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@router.put("/users/{user_id}", response_model=schema.UserInDB)
def update_user(user_id: int, user: schema.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user_update=user)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db=db, user_id=user_id)
    # Sure that invoke MQTT service again to synch up 
    return {"detail": "User deleted successfully"}

# Role routes
@router.post("/roles/", response_model=schema.RoleInDB)
def create_role(role: schema.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db=db, role=role)

@router.get("/roles/", response_model=List[schema.RoleInDB])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_roles(db, skip=skip, limit=limit)

@router.put("/roles/{role_id}", response_model=schema.RoleInDB)
def update_role(role_id: int, role: schema.RoleCreate, db: Session = Depends(get_db)):
    return crud.update_role(db=db, role_id=role_id, role_update=role)

@router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    crud.delete_role(db=db, role_id=role_id)
    return {"detail": "Role deleted successfully"}

# Product routes
@router.post("/products/", response_model=schema.ProductInDB, dependencies=[Depends(role_required("admin"))])
def create_product(product: schema.ProductCreate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user_with_roles)):
    # Example of multi-tenancy check, assuming product creation should be limited to the user's tenant
    if product.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Not authorized to create product for this tenant")
    return crud.create_product(db=db, product=product)

@router.get("/products/", response_model=List[schema.ProductInDB])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@router.put("/products/{product_id}", response_model=schema.ProductInDB)
def update_product(product_id: int, product: schema.ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db=db, product_id=product_id, product_update=product)

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    crud.delete_product(db=db, product_id=product_id)
    return {"detail": "Product deleted successfully"}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

