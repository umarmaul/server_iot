from pydantic import Field

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from pydantic import BaseModel

from ..database import Sessionlocal
from ..models import OpenWeather

router = APIRouter(
    prefix="/openweather",
    tags=["openweather"],
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

class OpenWeatherRequest(BaseModel):
    temperature: float = Field(description="Temperature", ge=-40.0, le=80.0)
    humidity: float = Field(description="Humidity", ge=0.0, le=100.0)

### Pages ###

### Endpoints ###
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_openweather(openweather_request: OpenWeatherRequest, db: Session = Depends(get_db)):
    if not openweather_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    openweather = OpenWeather(**openweather_request.dict())
    
    db.add(openweather)
    db.commit()
    return openweather

@router.get("/read_10", status_code=status.HTTP_200_OK)
async def read_openweather_10(db: Session = Depends(get_db)):
    try:
        openweather = db.query(OpenWeather).order_by(OpenWeather.timestamp.desc()).limit(10).all()
        return openweather
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/update/{openweather_id}", status_code=status.HTTP_200_OK)
async def update_openweather(openweather_id: int, openweather_request: OpenWeatherRequest, db: Session = Depends(get_db)):
    try:
        openweather = db.query(OpenWeather).filter(OpenWeather.id == openweather_id).first()
        if not openweather:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OpenWeather not found")
        
        openweather.temperature = openweather_request.temperature
        openweather.humidity = openweather_request.humidity
        db.commit()
        return openweather
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/delete/{openweather_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_openweather(openweather_id: int, db: Session = Depends(get_db)):
    try:
        openweather = db.query(OpenWeather).filter(OpenWeather.id == openweather_id).first()
        if not openweather:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OpenWeather not found")
        
        db.delete(openweather)
        db.commit()
        return {"message": "OpenWeather data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))