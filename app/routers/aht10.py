from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status
from pydantic import BaseModel, Field

from ..database import Sessionlocal
from ..models import AHT10

router = APIRouter(
    prefix="/aht10",
    tags=["aht10"],
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
        
class AHT10Request(BaseModel):
    temperature: float = Field(description="Temperature", ge=-40.0, le=80.0)
    humidity: float = Field(description="Humidity", ge=0.0, le=100.0)

### Endpoints ###
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_aht10(aht10_request: AHT10Request, db: Session = Depends(get_db)):
    if not aht10_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    aht10 = AHT10(**aht10_request.dict())
    
    db.add(aht10)
    db.commit()
    return aht10