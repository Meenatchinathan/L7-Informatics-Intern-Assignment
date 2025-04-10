from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(200))

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    __table_args__ = (UniqueConstraint('category', 'month', 'year', name='_category_month_year_uc'),)