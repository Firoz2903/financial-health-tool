from sqlalchemy import Column, Integer, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FinancialReport(Base):
    __tablename__ = "financial_reports"

    id = Column(Integer, primary_key=True, index=True)
    total_revenue = Column(Float)
    total_expense = Column(Float)
    profit = Column(Float)
    profit_margin = Column(Float)
    health_score = Column(Integer)
    ai_insights = Column(Text)
