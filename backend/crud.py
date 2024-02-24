# crud.py
from sqlalchemy.orm import Session
import model, schema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Tenant CRUD operations
def create_tenant(db: Session, tenant: schema.TenantCreate):
    db_tenant = model.Tenant(**tenant.dict())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

def get_tenants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Tenant).offset(skip).limit(limit).all()

def update_tenant(db: Session, tenant_id: int, tenant_update: schema.TenantCreate):
    db_tenant = db.query(model.Tenant).filter(model.Tenant.tenant_id == tenant_id).first()
    if not db_tenant:
        return None
    for var, value in vars(tenant_update).items():
        setattr(db_tenant, var, value) if value else None
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

def delete_tenant(db: Session, tenant_id: int):
    db_tenant = db.query(model.Tenant).filter(model.Tenant.tenant_id == tenant_id).first()
    if not db_tenant:
        return None
    db.delete(db_tenant)
    db.commit()
    return db_tenant

# User CRUD operations
def create_user(db: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = model.User(**user.dict(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: schema.UserCreate):
    db_user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if not db_user:
        return None
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()

def get_user_roles(db: Session, user_id: int):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if user:
        return [role.role_name for role in user.roles]
    return []

def user_has_tenant_access(db: Session, user_id: int, tenant_id: int):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    return user and user.tenant_id == tenant_id

# Role CRUD operations
def create_role(db: Session, role: schema.RoleCreate):
    db_role = model.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Role).offset(skip).limit(limit).all()

def update_role(db: Session, role_id: int, role_update: schema.RoleCreate):
    db_role = db.query(model.Role).filter(model.Role.role_id == role_id).first()
    if not db_role:
        return None
    for var, value in vars(role_update).items():
        setattr(db_role, var, value) if value else None
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    db_role = db.query(model.Role).filter(model.Role.role_id == role_id).first()
    if not db_role:
        return None
    db.delete(db_role)
    db.commit()
    return db_role

# Product CRUD operations
def create_product(db: Session, product: schema.ProductCreate):
    db_product = model.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_product_with_tenant_check(db: Session, product: schema.ProductCreate, user_id: int):
    # Ensure the user has access to the tenant they are trying to create a product for
    if not user_has_tenant_access(db, user_id=user_id, tenant_id=product.tenant_id):
        return None  # Or raise an exception based on your error handling policy
    return create_product(db, product)

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product_update: schema.ProductCreate):
    db_product = db.query(model.Product).filter(model.Product.product_id == product_id).first()
    if not db_product:
        return None
    for var, value in vars(product_update).items():
        setattr(db_product, var, value) if value else None
    db.commit()
    # TODO: Invoke MQTT to synch up the state 
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(model.Product).filter(model.Product.product_id == product_id).first()
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    return db_product
