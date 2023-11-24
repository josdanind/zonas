# Standard library
import hashlib

# Passlib
from passlib.context import CryptContext


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_sha256(password: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))

    return sha256.hexdigest()
