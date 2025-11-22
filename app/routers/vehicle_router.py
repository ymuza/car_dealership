from fastapi import APIRouter, HTTPException, Path
from typing import List, Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from ..services.vehicles_service import VehicleService
from ..schemas.schemas import VehicleBase
from ..db.session import get_db


router = APIRouter(prefix="/Vehicles", tags=["vehicles"])
db_dependency = Annotated[Session, Depends(get_db)]




@router.get("/vehicles", response_model=List[VehicleBase])
async def get_dealerships(db: db_dependency):
    vehicle_service = VehicleService(db)
    return await vehicle_service.get_vehicles()