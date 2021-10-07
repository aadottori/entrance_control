from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
import uvicorn
import qr_code_generator
import datetime

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tickets", tags = ["tickets"])
def get_all(db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).all()
    return tickets


@app.post("/tickets", tags = ["tickets"])
def create_ticket(db: Session = Depends(get_db)):
    new_ticket = models.Ticket(ticket=str(qr_code_generator.create_qr_code()),
                                entrance_time=datetime.datetime.now(datetime.timezone.utc),
                                exit_time=datetime.datetime.now(datetime.timezone.utc), 
                                paid=False, 
                                exited=False)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


@app.get("/tickets/{id}", response_model=schemas.ShowTicket, tags = ["tickets"])
def get_single_ticket(id, response:Response, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket with id {id} not available.")
    return ticket


@app.delete("/ticket/{id}", status_code=status.HTTP_204_NO_CONTENT, tags = ["tickets"])
def delete_ticket(id, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == id)
    if not ticket.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket with id {id} not available.")
    ticket.delete(synchronize_session=False)
    db.commit()
    return "Done"


@app.put('/ticket/{id}', status_code=status.HTTP_202_ACCEPTED, tags = ["tickets"]) 
def update_ticket(id, request: schemas.Ticket, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == id)
    if not ticket.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not available.")
    ticket.update(request.dict()) 
    db.commit() 
    return "Updated"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
