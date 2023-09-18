from passlib.context import CryptContext

class AuthRepository:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_password_hash(self, password):
        return self.pwd_context.hash(password)
    