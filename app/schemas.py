from pydantic import BaseModel, Field


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
    text: str = Field(..., description="Le texte brut à analyser (ex: un article de presse).")

class AnalysisResult(BaseModel):
    category: str = Field(..., description="Catégorie prédite par Hugging Face (ex: Finance).")
    score: float = Field(..., description="Score de confiance associé à la catégorie.")
    summary: str = Field(..., description="Résumé concis généré par Gemini (max 60 mots).")
    tone: str = Field(..., description="Tonalité détectée par Gemini (ex: positif, négatif, neutre).")