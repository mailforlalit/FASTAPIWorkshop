from jose import jwt

SECRET_KEY = 'secret123'
ALGORITHM = 'HS256'

def create_token(data: dict): # used to create token
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str): # used to verify the token and return the payload if valid otherwise return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
