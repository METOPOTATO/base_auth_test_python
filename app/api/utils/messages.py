class RESPONSE_ERRORS:
    DEFAULT = 'Error'
    USER_NOT_FOUND = 'User is not founded'
    WRONG_PW = 'Password is not correct'
    INVALID_DATA = 'Data is invalid'
    EMAIL_EXIST = 'This email already used'
    TOKEN_NOT_FOUNDED = 'This token is not founded in database'
    USER_IS_NOT_ACTIVE = 'This account is not active'


class RESPONSE_OK:
    DEFAULT = 'OK'


class VALIDATION_ERRORS:
    INVALID_EMAIL_FORM = 'The provided email is not correct'
    PASSWORD_TOO_SHORT = 'Password is too short'
