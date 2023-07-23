"""
    Module for the Assessment model.
"""

from datetime import datetime
from bson.objectid import ObjectId

class Assessment:
    def __init__(self, assessment: str, user_id: ObjectId) -> None:
        self.assement = assessment
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

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