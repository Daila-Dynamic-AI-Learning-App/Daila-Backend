"""
User model
"""
from models.basemodel import BaseModel
from datetime import datetime

DATA = ["email", "hashed_password", "username", "country"]

class User(BaseModel):
    """
        User class for mongodb collection
    """
    def __init__(self, *args, **kwargs) -> None:
        if kwargs:
            for key, val in kwargs.items():
                if key in DATA:
                    setattr(self, key, val)
        super().__init__(args, kwargs)

    def to_dict(self):
        """
            returns a dictionary representation of the object
        """
        return {
            'email': self.email,
            'hashed_password': self.hashed_password,
            'username': self.username,
            'country': self.country,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }