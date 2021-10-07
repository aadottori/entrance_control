from typing import List, Optional
from pydantic import BaseModel
import datetime


class TicketBase(BaseModel):
    ticket: str
    entrance_time: datetime.datetime
    exit_time: datetime.datetime
    paid: bool
    exited: bool


class Ticket(TicketBase):
    class Config():
        orm_mode = True


class ShowTicket(Ticket):
    ticket: str
    entrance_time: datetime.datetime
    exit_time: datetime.datetime
    paid: bool
    exited: bool
    class Config():
        orm_mode = True