# app/main.py
from fastapi import FastAPI
from app import deps

# importa routers (Python cargará app.routers.auth, app.routers.users, etc.)
from app.routers import auth, user, department, position, shift, device, attendance, holiday, audit_log

app = FastAPI(title="Attendance System")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(department.router)
app.include_router(position.router)
app.include_router(shift.router)
app.include_router(device.router)
app.include_router(attendance.router)
app.include_router(holiday.router)
app.include_router(audit_log.router)

@app.get("/health")
def health():
    return {"status": "ok"}
