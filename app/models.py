from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey

class Item(Base):
  __tablename__ = 'items'

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(length=255), nullable=False)
  content = Column(String())
  public = Column(Boolean, default=False, nullable=False)
  rating = Column(Integer, default=0, nullable=False)
