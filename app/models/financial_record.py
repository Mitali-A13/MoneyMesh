from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.db.database import Base


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income / expense
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
