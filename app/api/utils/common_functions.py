import re
from .messages import VALIDATION_ERRORS


def _validate_email(email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if re.fullmatch(pattern, email):
        return True
    return VALIDATION_ERRORS.INVALID_EMAIL_FORM


def _validate_password(password):
    if len(password) < 6:
        return VALIDATION_ERRORS.PASSWORD_TOO_SHORT
    return True
