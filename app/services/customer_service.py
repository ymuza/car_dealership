from fastapi import APIRouter
from typing import List

from fastapi import Depends
from app.db.models.models import Vehicle
from sqlalchemy.orm import Session
from typing import Annotated
from passlib.context import CryptContext
from app.db.session import get_db
from app.db.models.models import Customer



router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

db_dependency = Annotated[Session, Depends(get_db)]



class CustomersService:
    def __init__(self, db: db_dependency):
        self.db = db

    async def get_vehicles(self):
        return self.db.query(Customer).all()


