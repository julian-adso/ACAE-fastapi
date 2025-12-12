# app/routers/__init__.py
# Intencionalmente NO importamos submódulos aquí para evitar imports circulares.
# Los submódulos serán importados por `from app.routers import <name>` cuando sea necesario.

__all__ = [
    "auth",
    "users",
    "departments",
    "positions",
    "shifts",
    "devices",
    "attendance",
    "holidays",
    "audit_logs",
]
