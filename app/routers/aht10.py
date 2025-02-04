from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from starlette import status
from pydantic import BaseModel, Field

from ..database import Sessionlocal
from ..models import AHT10

templates = Jinja2Templates(directory="app/templates")

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

### Pages ###

### Endpoints ###
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_aht10(aht10_request: AHT10Request, db: Session = Depends(get_db)):
    if not aht10_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    aht10 = AHT10(**aht10_request.dict())
    
    db.add(aht10)
    db.commit()
    return aht10

@router.get("/read_10", status_code=status.HTTP_200_OK)
async def read_aht10_10(db: Session = Depends(get_db)):
    try:
        aht10 = db.query(AHT10).order_by(AHT10.timestamp.desc()).limit(10).all()
        return aht10
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))