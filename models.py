from sqlalchemy import Column, Integer, String, Date, func, Float

from db import Base


class Currency(Base):
    __tablename__ = "Currency"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=func.now())
    first_currency = Column(String(3))
    second_currency = Column(String(3))
    price = Column(Float)
