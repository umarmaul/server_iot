from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from starlette import status
from pydantic import BaseModel, Field

from ..database import Sessionlocal
from ..models import AHT10
from datetime import datetime

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
@router.get("/")
async def aht10(request: Request, db: Session = Depends(get_db)):
    aht10_records = db.query(AHT10).all()
    for record in aht10_records:
        record.timestamp = datetime.strftime(record.timestamp, "%Y-%m-%d %H:%M")
    return templates.TemplateResponse("aht10.html", {"request": request, "aht10": aht10_records})

### Endpoints ###
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_aht10(aht10_request: AHT10Request, db: Session = Depends(get_db)):
    if not aht10_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    aht10 = AHT10(**aht10_request.dict())
    
    db.add(aht10)
    db.commit()
    return aht10