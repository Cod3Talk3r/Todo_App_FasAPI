from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "User Not Found!"
    
    pass


class TodoNotFound(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "Todo Not Found!"
    
    pass


class UNAUTHORIZED(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Not authenticated"
    
    pass


class TokenIsNotValid(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Token is not valid!"
    
    pass


class WrongPassword(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Wrong password!"
    
    pass


class ExistingUser(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "This User is exist, please change your Username!"
    
    pass


class ExistingEmail(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "This Email is exist, please change your Email!"
    
    pass