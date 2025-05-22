from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

DATABASE_URL = "postgresql://shared:password@shared-db:5432/shared"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# --- Users ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class UserCreate(BaseModel):
    name: str

# --- Orders ---
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)

class OrderCreate(BaseModel):
    item: str

Base.metadata.create_all(bind=engine)

@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@app.get("/users")
def list_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

@app.post("/orders")
def create_order(order: OrderCreate):
    db = SessionLocal()
    db_order = Order(item=order.item)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    db.close()
    return db_order

@app.get("/orders")
def list_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    return orders
