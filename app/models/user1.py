from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class User1(Base):
    __tablename__ = "user1s"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
