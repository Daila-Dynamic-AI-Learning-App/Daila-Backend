import re

def validateEmail(email: str) -> bool:
    """
        takes in the email of the user, checks if
        it is valid and returns a bool
    """
    # define pattern to search for in the email
    pattern = r'^[a-zA-Z0-9]+@\w+.[a-z]{3}'

    # check if email is a valid pattern
    if re.search(pattern, email):
        return True
    return False
