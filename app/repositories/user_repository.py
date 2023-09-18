from ..dependencies.dependencies import db_dependency
from ..models import Users
class UserRepository:
    
    def __init__(self, db: db_dependency):
        self.db = db
        
    def add(self, new_user: Users) -> Users:
        self.db.add(new_user)
        self.db.commit()
        return new_user
    
    def read_by_username(self, username: str) -> Users | None:
        return self.db.query(Users).filter(Users.username == username).first()
         