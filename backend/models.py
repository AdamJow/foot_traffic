from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class FootTraffic(Base):
    __tablename__ = "foot_traffic"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True, nullable=False)
    store_id = Column(String, index=True, nullable=False)
    store_name = Column(String, nullable=False)
    people_count = Column(Integer, nullable=False)
