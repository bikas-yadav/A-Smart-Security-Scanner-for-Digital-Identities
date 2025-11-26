import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, Float, Text
from .database import Base

class EntityType(str, enum.Enum):
    email = "email"
    phone = "phone"
    username = "username"
    domain = "domain"
    breach = "breach"

class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(EntityType), nullable=False, index=True)
    value = Column(String(255), nullable=False, index=True, unique=False)
    description = Column(Text, nullable=True)
    risk_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
