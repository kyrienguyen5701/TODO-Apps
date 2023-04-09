from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Todo(Base):
  __tablename__ = 'TODOS'
  
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  finished = Column(Boolean, default=False)
  