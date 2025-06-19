from passlib.context import CryptContext

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(p: str) -> str:
    return _pwd.hash(p)


def verify_password(raw: str, hashed: str) -> bool:
    return _pwd.verify(raw, hashed)
