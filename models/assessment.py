"""
    Module for the Assessment model.
"""
from models.basemodel import BaseModel

DATA = ["assessment", "user_id"]


class Assessment(BaseModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        if kwargs:
            for key, val in kwargs.items():
                if key in DATA:
                    setattr(self, key, val)

    def toDict(self):
        """
            returns a dict representation of the object
        """
        return {
            'assessment': self.assessment,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
