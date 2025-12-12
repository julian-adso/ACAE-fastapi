# app/crud/devices.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate

def get_device(db: Session, id: int) -> Optional[Device]:
    return db.query(Device).filter(Device.id == id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100) -> List[Device]:
    return db.query(Device).offset(skip).limit(limit).all()

def create_device(db: Session, payload: DeviceCreate) -> Device:
    d = Device(identifier=payload.identifier, location=payload.location)
    db.add(d); db.commit(); db.refresh(d)
    return d

def update_device(db: Session, device: Device, payload: DeviceUpdate) -> Device:
    data = payload.dict(exclude_unset=True)
    for k,v in data.items():
        setattr(device, k, v)
    db.add(device); db.commit(); db.refresh(device)
    return device

def delete_device(db: Session, device: Device):
    db.delete(device); db.commit()
