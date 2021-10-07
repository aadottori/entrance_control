from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket = Column(String)
    entrance_time = Column(DateTime)
    exit_time = Column(DateTime)
    paid = Column(Boolean)
    exited = Column(Boolean)
