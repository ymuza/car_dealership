from fastapi import APIRouter, HTTPException, Path
from typing import List, Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from ..services.vehicles_service import VehicleService
from ..schemas.schemas import CustomerBase
from ..db.session import get_db


router = APIRouter(prefix="/Customers", tags=["customers"])
db_dependency = Annotated[Session, Depends(get_db)]




@router.get("/customers", response_model=List[CustomerBase])
async def get_dealerships(db: db_dependency):
    vehicle_service = VehicleService(db)
    return await vehicle_service.get_vehicles()