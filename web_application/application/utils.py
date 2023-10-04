import re


def validate_password(password):
    """
    Function to validate password during user registration.
    :param password: password for user
    """
    errors = {}

    if len(password) < 8:
        errors["password"] = ["Password must have at least 8 characters."]

    if not any(char.isupper() for char in password):
        errors["password"] = ["Password must have at least one capital letter."]

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors["password"] = ["Password must have at least one special character."]
    if not any(char.isdigit() for char in password):
        errors["password"] = ["Password must have at least one numeric character."]

    if not any(char.isalpha() for char in password):
        errors["password"] = ["Password must contain alphabetic characters."]

    return errors
