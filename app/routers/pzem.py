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

### Endpoints ###
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_pzem(pzem_request: PzemRequest, db: Session = Depends(get_db)):
    if not pzem_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    pzem = Pzem(**pzem_request.dict())
    
    db.add(pzem)
    db.commit()
    return pzem