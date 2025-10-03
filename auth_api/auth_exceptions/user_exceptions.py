import logging
from typing import Optional

from auth_api.auth_exceptions.base_exception import DukanBaseException


class UserNotFoundError(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "This user is not registered. Please register as new user."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class UserAlreadyVerifiedError(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "This user is already verified."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class UserNotVerifiedError(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "This user is not verified. Please verify your email first."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class EmailNotSentError(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Verification Email could not be sent."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class OTPNotVerifiedError(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "OTP did not match."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class UserAuthenticationFailedError(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Password is invalid."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class UserNotAuthenticatedError(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "The user is not authenticated, please re-login."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class PasswordNotMatchError(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Password1 and Password2 do not match."
        else:
            super().__init__(msg)
        logging.error(self.msg)



class NotValidUserID(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "User not found."
        else:
            super().__init__(msg)
        logging.error(self.msg)


class NotValidUserEmail(DukanBaseException):
    def __init__(self, msg: Optional[str] = None):
        if not msg:
            self.msg = "Please provide a valid email."
        else:
            super().__init__(msg)
        logging.error(self.msg)
