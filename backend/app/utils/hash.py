from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    password = password[:72]
    return pwd_context.hash(password)


# 🔍 VERIFY PASSWORD
def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)
