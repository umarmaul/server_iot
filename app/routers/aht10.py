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

@router.get("/read_10", status_code=status.HTTP_200_OK)
async def read_aht10_10(db: Session = Depends(get_db)):
    try:
        aht10 = db.query(AHT10).order_by(AHT10.timestamp.desc()).limit(10).all()
        return aht10
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/update/{aht_id}", status_code=status.HTTP_200_OK)
async def update_aht10(aht10_id: int, aht10_request: AHT10Request, db: Session = Depends(get_db)):
    try:
        aht10 = db.query(AHT10).filter(AHT10.id == aht10_id).first()
        if not aht10:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AHT10 not found")
        
        aht10.temperature = aht10_request.temperature
        aht10.humidity = aht10_request.humidity
        db.commit()
        return aht10
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.delete("/delete/{aht10_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aht10(aht10_id: int, db: Session = Depends(get_db)):
    try:
        aht10 = db.query(AHT10).filter(AHT10.id == aht10_id).first()
        if not aht10:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AHT10 not found")
        
        db.delete(aht10)
        db.commit()
        return {"message": "AHT10 data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))