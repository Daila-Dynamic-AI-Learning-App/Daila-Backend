from bcrypt import hashpw, gensalt
from uuid import uuid4

def hash_password(password: str) -> bytes:
    """
    returns salted hash of the input password
    """
    encoded_pass = password.encode("utf-8")
    return hashpw(encoded_pass, gensalt())


def generate_uuid() -> str:
    """
    generates a new unique string id
    """
    return str(uuid4())
