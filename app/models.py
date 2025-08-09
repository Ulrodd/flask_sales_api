from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    sales = relationship("Sale", back_populates="customer")

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Numeric)
    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    invoice_no = Column(String)
    date = Column(Date)
    quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey('product.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))

    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
