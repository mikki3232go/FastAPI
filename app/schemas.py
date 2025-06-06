from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import FacilityType

class FacilityBase(BaseModel):
    name: str
    type: FacilityType
    location: str
    capacity: Optional[int] = None
    description: Optional[str] = None

class FacilityCreate(FacilityBase):
    pass

class FacilityUpdate(FacilityBase):
    name: Optional[str] = None
    type: Optional[FacilityType] = None
    location: Optional[str] = None

class Facility(FacilityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ReservationBase(BaseModel):
    facility_id: int
    user_name: str
    user_phone: str
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(ReservationBase):
    facility_id: Optional[int] = None
    user_name: Optional[str] = None
    user_phone: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class Reservation(ReservationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 