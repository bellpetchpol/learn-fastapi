from sqlalchemy import func
from ..dependencies import db_dependency
from ..models import Users
class UserRepository:
    
    def __init__(self, db: db_dependency):
        self.db = db
        
    def add(self, new_user: Users) -> Users:
        new_user.username = new_user.username.lower()
        self.db.add(new_user)
        self.db.commit()
        return new_user
    
    def read_by_username(self, username: str) -> Users | None:
        return self.db.query(Users).filter(func.lower(Users.username) == username.lower()).first()
    
    def read_by_id(self, user_id: int) -> Users | None:
        return self.db.query(Users).filter(Users.id == user_id).first()
         