from pydantic import Field

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from pydantic import BaseModel

from ..database import Sessionlocal
from ..models import Camera

router = APIRouter(
    prefix="/camera",
    tags=["camera"],
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

class CameraRequest(BaseModel):
    occupant: int = Field(description="Occupant(s)", ge=0)

### Pages ###

### Endpoints ###
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_camera(camera_request: CameraRequest, db: Session = Depends(get_db)):
    if not camera_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
    camera = Camera(**camera_request.dict())
    
    db.add(camera)
    db.commit()
    return camera

@router.get("/read_10", status_code=status.HTTP_200_OK)
async def read_camera_10(db: Session = Depends(get_db)):
    try:
        camera = db.query(Camera).order_by(Camera.timestamp.desc()).limit(10).all()
        return camera
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/update/{camera_id}", status_code=status.HTTP_200_OK)
async def update_camera(camera_id: int, camera_request: CameraRequest, db: Session = Depends(get_db)):
    try:
        camera = db.query(Camera).filter(Camera.id == camera_id).first()
        if not camera:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
        
        camera.occupant = camera_request.occupant
        db.commit()
        return camera
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.delete("/delete/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(camera_id: int, db: Session = Depends(get_db)):
    try:
        camera = db.query(Camera).filter(Camera.id == camera_id).first()
        if not camera:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
        
        db.delete(camera)
        db.commit()
        return {"message": "Camera data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))