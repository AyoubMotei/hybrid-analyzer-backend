from pydantic import BaseModel


# Schémas Utilisateur

class UserCreate(BaseModel):
    username: str 
    password: str  

class UserLogin(UserCreate):
    pass 

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


#  Schémas d'Analyse IA


class AnalysisInput(BaseModel):
    text: str 

class AnalysisResult(BaseModel):
    summary: str 
    tone: str
    category: str  
    score: float 
    
  