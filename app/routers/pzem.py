from pydantic import Field

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from pydantic import BaseModel

from ..database import Sessionlocal
from ..models import Pzem

router = APIRouter(
    prefix="/pzem",
    tags=["pzem"],
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

class PzemRequest(BaseModel):
    voltage: float = Field(description="Voltage", ge=0.0)
    current: float = Field(description="Current", ge=0.0)
    power: float = Field(description="Power", ge=0.0)
    energy: float = Field(description="Energy", ge=0.0)
    frequency: float = Field(description="Frequency", ge=0.0)
    power_factor: float = Field(description="Power Factor", ge=0.0)

### Pages ###

### Endpoints ###
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_pzem(pzem_request: PzemRequest, db: Session = Depends(get_db)):
    if not pzem_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    pzem = Pzem(**pzem_request.dict())
    
    db.add(pzem)
    db.commit()
    return pzem

@router.get("/read_10", status_code=status.HTTP_200_OK)
async def read_pzem_10(db: Session = Depends(get_db)):
    try:
        pzem = db.query(Pzem).order_by(Pzem.timestamp.desc()).limit(10).all()
        return pzem
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/update/{pzem_id}", status_code=status.HTTP_200_OK)
async def update_pzem(pzem_id: int, pzem_request: PzemRequest, db: Session = Depends(get_db)):
    try:
        pzem = db.query(Pzem).filter(Pzem.id == pzem_id).first()
        if not pzem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pzem not found")
        
        pzem.temperature = pzem_request.temperature
        pzem.humidity = pzem_request.humidity
        db.commit()
        return pzem
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.delete("/delete/{pzem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pzem(pzem_id: int, db: Session = Depends(get_db)):
    try:
        pzem = db.query(Pzem).filter(Pzem.id == pzem_id).first()
        if not pzem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pzem not found")
        
        db.delete(pzem)
        db.commit()
        return {"message": "Pzem data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))