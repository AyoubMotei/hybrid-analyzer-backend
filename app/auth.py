from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status

from fastapi.security import HTTPBearer, HTTPBasicCredentials

import os
from dotenv import load_dotenv 

load_dotenv()

JWT_SECRET_KEY= os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


# Hachage du Mot de Passe (Argon2)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) :
    return pwd_context.verify(plain_password, hashed_password)


#  Gestion du JWT (Création et Décodage)


def create_access_token(data: dict) :
    to_encode = data.copy()
    
    encoded_jwt = jwt.encode(
        to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token):

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if not payload.get("sub"):
            raise JWTError("sub manquant")
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Extraction du token 

bearer_scheme = HTTPBearer()  

async def get_current_user(
    creds: HTTPBasicCredentials = Depends(bearer_scheme),):
   
    token = creds.credentials  
    payload = decode_access_token(token)  
    return payload.get("sub")