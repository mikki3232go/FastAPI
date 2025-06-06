from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/new")
async def new_reservation(
    request: Request,
    facility_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    facility = None
    facilities = None
    
    if facility_id is not None:
        facility = db.query(models.Facility).filter(models.Facility.id == facility_id).first()
        if not facility:
            raise HTTPException(status_code=404, detail="Facility not found")
    else:
        facilities = db.query(models.Facility).all()

    return templates.TemplateResponse(
        "reservations/new.html",
        {"request": request, "facility": facility, "facilities": facilities}
    )

@router.get("/{reservation_id}/edit")
async def edit_reservation(
    request: Request,
    reservation_id: int,
    db: Session = Depends(get_db)
):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return templates.TemplateResponse(
        "reservations/edit.html",
        {"request": request, "reservation": reservation}
    )

@router.get("/", response_model=List[schemas.Reservation])
def get_reservations(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    reservations = db.query(models.Reservation).offset(skip).limit(limit).all()
    return templates.TemplateResponse(
        "reservations/list.html",
        {"request": request, "reservations": reservations}
    )

@router.post("/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    # 시설 존재 여부 확인
    facility = db.query(models.Facility).filter(models.Facility.id == reservation.facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    
    # 시간 중복 체크
    existing_reservation = db.query(models.Reservation).filter(
        models.Reservation.facility_id == reservation.facility_id,
        models.Reservation.start_time <= reservation.end_time,
        models.Reservation.end_time >= reservation.start_time
    ).first()
    
    if existing_reservation:
        raise HTTPException(status_code=400, detail="Time slot already reserved")
    
    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.get("/{reservation_id}", response_model=schemas.Reservation)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.put("/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(
    reservation_id: int,
    reservation: schemas.ReservationUpdate,
    db: Session = Depends(get_db)
):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    for key, value in reservation.dict(exclude_unset=True).items():
        setattr(db_reservation, key, value)
    
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    db.delete(reservation)
    db.commit()
    return {"message": "Reservation deleted successfully"} 