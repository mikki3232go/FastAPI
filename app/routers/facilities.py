from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/facilities",
    tags=["facilities"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_model=List[schemas.Facility])
def get_facilities(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    facilities = db.query(models.Facility).offset(skip).limit(limit).all()
    return templates.TemplateResponse(
        "facilities/list.html",
        {"request": request, "facilities": facilities}
    )

@router.post("/", response_model=schemas.Facility)
def create_facility(facility: schemas.FacilityCreate, db: Session = Depends(get_db)):
    db_facility = models.Facility(**facility.dict())
    db.add(db_facility)
    db.commit()
    db.refresh(db_facility)
    return db_facility

@router.get("/{facility_id}", response_model=schemas.Facility)
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    facility = db.query(models.Facility).filter(models.Facility.id == facility_id).first()
    if facility is None:
        raise HTTPException(status_code=404, detail="Facility not found")
    return facility

@router.put("/{facility_id}", response_model=schemas.Facility)
def update_facility(
    facility_id: int,
    facility: schemas.FacilityUpdate,
    db: Session = Depends(get_db)
):
    db_facility = db.query(models.Facility).filter(models.Facility.id == facility_id).first()
    if db_facility is None:
        raise HTTPException(status_code=404, detail="Facility not found")
    
    for key, value in facility.dict(exclude_unset=True).items():
        setattr(db_facility, key, value)
    
    db.commit()
    db.refresh(db_facility)
    return db_facility

@router.delete("/{facility_id}")
def delete_facility(facility_id: int, db: Session = Depends(get_db)):
    facility = db.query(models.Facility).filter(models.Facility.id == facility_id).first()
    if facility is None:
        raise HTTPException(status_code=404, detail="Facility not found")
    
    db.delete(facility)
    db.commit()
    return {"message": "Facility deleted successfully"} 