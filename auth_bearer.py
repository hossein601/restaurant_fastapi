from fastapi import Request,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error:bool=True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials : HTTPAuthorizationCredentials() = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403,detail='Not Authorized')
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,detail='Not Authorized')
            return credentials.credentials
        else:
            raise HTTPException(status_code=403,detail='Not Authorized')

    def verify_jwt(self,token:str)->bool:
        isTokenValid : bool = False
        try:
            payload = jwt.get_unverified_claims(token)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


