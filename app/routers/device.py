# app/routers/devices.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import deps
from app.crud import device as crud_devices
from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate

router = APIRouter(prefix="/devices", tags=["devices"])

@router.post("/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
def create_device(payload: DeviceCreate, db: Session = Depends(deps.get_db)):
    return crud_devices.create_device(db, payload)

@router.get("/", response_model=List[DeviceRead])
def list_devices(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud_devices.get_devices(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=DeviceRead)
def get_device(id: int, db: Session = Depends(deps.get_db)):
    d = crud_devices.get_device(db, id)
    if not d:
        raise HTTPException(status_code=404, detail="device not found")
    return d

@router.patch("/{id}", response_model=DeviceRead)
def patch_device(id: int, payload: DeviceUpdate, db: Session = Depends(deps.get_db)):
    d = crud_devices.get_device(db, id)
    if not d:
        raise HTTPException(status_code=404, detail="device not found")
    return crud_devices.update_device(db, d, payload)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(id: int, db: Session = Depends(deps.get_db)):
    d = crud_devices.get_device(db, id)
    if not d:
        raise HTTPException(status_code=404, detail="device not found")
    crud_devices.delete_device(db, d)
    return
