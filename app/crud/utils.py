# app/crud/utils.py
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from typing import Optional
from sqlalchemy.orm import Session

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(stored_hash: str, password: str, legacy_hash: Optional[str]=None, legacy_algo: Optional[str]=None, db: Optional[Session]=None, user_obj: Optional[object]=None) -> bool:
    """
    Verifica password contra stored_hash (PBKDF2/bcrypt) o legacy (sha1).
    Si legacy coincide y se proporcionó user_obj y db, hace rehash y actualiza.
    """
    try:
        if check_password_hash(stored_hash or "", password):
            return True
    except Exception:
        pass

    # fallback legacy SHA1
    if legacy_hash and legacy_algo == "sha1":
        if legacy_hash == hashlib.sha1(password.encode("utf-8")).hexdigest():
            # optionally upgrade: if user_obj and db provided, rehash and store
            if user_obj is not None and db is not None:
                user_obj.password_hash = generate_password_hash(password)
                user_obj.legacy_password_hash = None
                user_obj.legacy_hash_algorithm = None
                db.add(user_obj)
                db.commit()
            return True
    return False
