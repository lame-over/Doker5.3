from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

DATABASE_URL = "postgresql://order:password@order-db:5432/orders"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)

class OrderCreate(BaseModel):
    item: str

Base.metadata.create_all(bind=engine)

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
