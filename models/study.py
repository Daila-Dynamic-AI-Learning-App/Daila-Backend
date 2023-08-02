"""
    Study model
"""
from models.basemodel import BaseModel


DATA = ["assessment_id", "user_id", "interest", "year"]


class Study(BaseModel):
    """
        Study class for mongodb collection
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        if kwargs:
            for key, val in kwargs.items():
                if key in DATA:
                    setattr(self, key, val)

    def to_dict(self):
        """
            returns a dictionary representation of the object
        """
        return {
            'assessment_id': self.assessment_id,
            'user_id': self.user_id,
            'interest': self.interest,
            'year': self.year,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
