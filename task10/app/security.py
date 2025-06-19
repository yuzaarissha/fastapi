from passlib.context import CryptContext

_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(p: str) -> str:
    return _ctx.hash(p)


def verify_password(raw: str, hashed: str) -> bool:
    return _ctx.verify(raw, hashed)
