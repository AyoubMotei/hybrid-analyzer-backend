from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db 
 
from .schemas import UserCreate, UserLogin , AnalysisInput, AnalysisResult, Token
from app.models import User

from app.auth import create_access_token, hash_password, verify_password, get_current_user

from app.services.gemini import summarize_and_analyze_tone

from .database import get_db

from dotenv import load_dotenv
import os

load_dotenv()


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hybrid Analyser API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API opérationnelle"}



@app.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.username == user.username).first()
    
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    

    hashed_pwd = hash_password(user.password)
    
    
    db_user = User(username=user.username, password_hash=hashed_pwd)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    token = create_access_token(data={"sub":db_user.username})

    return {"access_token": token, "token_type": "bearer"}


@app.post("/analyser")
def analyse(text:str , current_user: User = Depends(get_current_user)):
    # print(f"Analyse demandée par l'utilisateur: {current_user}")
    gemini_response=summarize_and_analyze_tone(text)
    return gemini_response
    
    

@app.get("/test-env")
def test_env():
    return {
        "hf_key_configured": bool(os.getenv("HF_TOKEN")),
        "jwt_secret_configured": bool(os.getenv("JWT_SECRET_KEY")),
        "hf_key_preview": os.getenv("HF_TOKEN", "")[:10] + "..." if os.getenv("HF_TOKEN") else "None"
    }