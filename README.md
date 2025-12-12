# Hybrid Analyzer - Backend API

[![Backend](https://img.shields.io/badge/Backend-Python%2FFastAPI-green)](https://github.com/AyoubMotei/hybrid-analyzer-backend)
[![Frontend](https://img.shields.io/badge/Frontend-HTML%2FJS%2FCSS-blue)](https://github.com/AyoubMotei/hybrid-analyzer-frontend)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-316192.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> API REST d'orchestration IA hybride combinant la classification Zero-Shot (Hugging Face) et la synthèse contextuelle (Google Gemini) pour l'analyse automatisée d'articles de veille.

---

##  Vue d'ensemble

**Hybrid Analyzer Backend** est une API REST construite avec FastAPI qui orchestre deux services d'intelligence artificielle pour automatiser l'analyse d'articles de presse et de documents textuels.

### Problématique

Les agences de media monitoring traitent des centaines d'articles quotidiennement. Le processus manuel est :
- **Lent** : Plusieurs minutes par article
- **Coûteux** : Dépendance à l'expertise humaine
- **Peu fiable** : Erreurs de catégorisation
- **Non scalable** : Impossible à industrialiser

### Solution

Une plateforme d'orchestration IA qui combine :
1. **Classification Zero-Shot** (Hugging Face - BART-Large-MNLI)
2. **Synthèse Contextuelle & Analyse de Ton** (Google Gemini Flash 2.5)

### Résultat

```
Input: "Apple Inc. a annoncé des résultats financiers record..."

Output:
{
  "category": "Finance",
  "score": 0.94,
  "summary": "Apple annonce des résultats trimestriels exceptionnels...",
  "tone": "positif"
}
```

---

## Architecture

### Architecture globale

```
┌──────────────────────────────────────────────────────────────┐
│                    CLIENT (Frontend)                          │
│              HTML/JavaScript/CSS Application                  │
└────────────────────┬─────────────────────────────────────────┘
                     │ HTTP/JSON + JWT
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                   BACKEND API (FastAPI)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Auth       │  │  Database    │  │  Services    │       │
│  │  (JWT)       │  │ (PostgreSQL) │  │ (HF+Gemini)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────┬─────────────────┬───────────────────────┘
                     │                 │
        ┌────────────┴────────┐       │
        ▼                     ▼        ▼
┌──────────────┐    ┌──────────────┐  ┌──────────────┐
│ Hugging Face │    │   Gemini     │  │  PostgreSQL  │
│     API      │    │     API      │  │   Database   │
│   (BART)     │    │ (Flash 2.5)  │  │   (Users)    │
└──────────────┘    └──────────────┘  └──────────────┘
```

### Flux d'orchestration IA

```
┌─────────────────────────────────────────────────────────────┐
│                    ANALYSE WORKFLOW                          │
└─────────────────────────────────────────────────────────────┘

1. POST /analyse + JWT Token
          │
          ▼
2. Validation JWT & extraction user
          │
          ▼
3. ÉTAPE 1: Hugging Face Classification
   ├─→ Model: facebook/bart-large-mnli
   ├─→ Input: Texte brut
   ├─→ Candidates: [Finance, RH, IT, ...]
   └─→ Output: (category, score)
          │
          ▼
4. ÉTAPE 2: Gemini Synthesis (contextualisé)
   ├─→ Model: gemini-2.5-flash
   ├─→ Input: Texte + Catégorie (de HF)
   ├─→ Prompt Engineering avec contexte
   └─→ Output: {summary, tone}
          │
          ▼
5. AGRÉGATION des résultats
   {
     "category": "Finance",
     "score": 0.94,
     "summary": "...",
     "tone": "positif"
   }
          │
          ▼
6. RETOUR au client (JSON)
```

### Architecture modulaire

```
app/
├── main.py              # Point d'entrée FastAPI (routes)
├── models.py            # Modèles SQLAlchemy (User)
├── schemas.py           # Schémas Pydantic (validation)
├── database.py          # Configuration PostgreSQL
├── auth.py              # Sécurité JWT + Hashing
└── services/
    ├── huggingface.py   # Classification Zero-Shot
    └── gemini.py        # Synthèse + Analyse de ton
```

---

##  Fonctionnalités

### Authentification & Autorisation
- ✅ Inscription utilisateur avec hashing Argon2
- ✅ Connexion avec génération de token JWT
- ✅ Protection des endpoints par Bearer Token
- ✅ Validation automatique des tokens expirés

###  Orchestration IA
- ✅ Classification Zero-Shot (8 catégories)
- ✅ Score de confiance pour chaque prédiction
- ✅ Synthèse contextuelle intelligente (max 60 mots)
- ✅ Détection automatique du ton (positif/négatif/neutre)
- ✅ Gestion des erreurs API (timeout, rate limit)
- ✅ Logging complet des requêtes IA

###  Gestion des données
- ✅ Stockage sécurisé des utilisateurs (PostgreSQL)
- ✅ Migrations de base de données automatiques

###  Robustesse
- ✅ Gestion d'erreurs complète (try/catch)
- ✅ Validation de schémas avec Pydantic
- ✅ Tests unitaires avec mocks (pytest)
- ✅ Tests d'intégration end-to-end
- ✅ CORS configuré pour le frontend

---

## Stack technique

### Core Framework
- **FastAPI 0.100+** : Framework web moderne et performant
- **Python 3.8+** : Langage principal
- **Uvicorn** : Serveur ASGI pour production

### Intelligence Artificielle
- **Hugging Face Inference API** : Classification Zero-Shot
  - Modèle : `facebook/bart-large-mnli`
  - Technique : Natural Language Inference (NLI)
- **Google Gemini API** : Synthèse & Analyse
  - Modèle : `gemini-2.5-flash`
  - Configuration : JSON output, temperature 0.3

### Base de données
- **PostgreSQL 13+** : Base de données relationnelle
- **SQLAlchemy 2.0** : ORM Python
- **Psycopg2** : Driver PostgreSQL


### Sécurité
- **Passlib + Argon2** : Hashing des mots de passe
- **Python-Jose** : Gestion des tokens JWT
- **Python-dotenv** : Variables d'environnement

### Tests
- **Pytest** : Framework de tests
- **Pytest-mock** : Mocking des API externes
- **TestClient** : Tests d'intégration FastAPI

### DevOps
- **Docker** : Conteneurisation
- **Docker Compose** : Orchestration multi-services


---

##  Prérequis

### Logiciels requis
- **Python 3.8+** 
- **PostgreSQL 13+** 
- **Git** 
- **Docker & Docker Compose** 

### API Keys nécessaires

| Service | Description | Obtention |
|---------|-------------|-----------|
| **Hugging Face Token** | Classification Zero-Shot | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| **Gemini API Key** | Synthèse contextuelle | [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey) |


---

##  Installation

### Méthode 1 : Installation classique

#### 1. Cloner le repository

```bash
git clone https://github.com/AyoubMotei/hybrid-analyzer-backend.git
cd hybrid-analyzer-backend
```

#### 2️. Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3️. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Contenu de `requirements.txt` :**
```txt
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
pydantic
python-jose[cryptography]
passlib[argon2]
python-dotenv
google-generativeai
requests
pytest
pytest-mock
```

#### 4️. Configurer PostgreSQL

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base de données
CREATE DATABASE hybrid_analyzer_db;

# Créer un utilisateur (optionnel)
CREATE USER hybrid_user WITH PASSWORD 'votre_password';
GRANT ALL PRIVILEGES ON DATABASE hybrid_analyzer_db TO hybrid_user;
```

#### 5️. Configurer les variables d'environnement

Créez un fichier `.env` à la racine :

```bash
# Database Configuration
POSTGRES_USER=hybrid_user
POSTGRES_PASSWORD=votre_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=hybrid_analyzer_db

# JWT Configuration
JWT_SECRET_KEY=votre_secret_key_tres_securisee_ici
JWT_ALGORITHM=HS256

# API Keys
HF_TOKEN=hf_votre_token_huggingface
GEMINI_API_KEY=votre_api_key_gemini
```




## 📁 Structure du projet

```
hybrid-analyzer-backend/
│
├── 📁 app/                          # Package principal de l'application
│   ├── 📄 __init__.py               # Init du package
│   ├── 📄 main.py                   # Point d'entrée FastAPI + Routes
│   ├── 📄 models.py                 # Modèles SQLAlchemy (User)
│   ├── 📄 schemas.py                # Schémas Pydantic (validation)
│   ├── 📄 database.py               # Configuration PostgreSQL + Session
│   ├── 📄 auth.py                   # JWT + Hashing + Dependencies
│   │
│   └── 📁 services/                 # Services d'orchestration IA
│       ├── 📄 __init__.py
│       ├── 📄 huggingface.py        # Classification Zero-Shot
│       └── 📄 gemini.py             # Synthèse + Analyse de ton
│
├── 📁 tests/                        # Tests unitaires et d'intégration
   ├── 📄 __init__.py
   ├── 📄 conftest.py               # Configuration pytest
   ├── 📄 test_mock_huggingface.py  # Tests HF (mocké)
   ├── 📄 test_mock_gemini.py       # Tests Gemini (mocké)
   └── 📄 test_chainage_complet.py  # Tests end-to-end


```

### Description des modules principaux

#### `app/main.py` - Point d'entrée
```python
# Routes principales
- GET  /health          → Health check
- POST /register        → Inscription
- POST /login           → Connexion (JWT)
- POST /analyse         → Analyse IA (protégé)
- GET  /test-env        → Vérifier config (dev only)
```

#### `app/auth.py` - Sécurité
```python
# Fonctions
- hash_password()         → Hachage Argon2
- verify_password()       → Vérification hash
- create_access_token()   → Génération JWT
- decode_access_token()   → Décodage JWT
- get_current_user()      → Dependency injection
```

#### `app/services/huggingface.py` - Classification
```python
# Fonction principale
- classify_text(text) → (label, score)

# Catégories supportées
["Finance", "RH", "IT", "Opérations", 
 "Marketing", "Juridique", "Sport", "Général"]
```

#### `app/services/gemini.py` - Synthèse
```python
# Fonction principale
- summarize_and_analyze_tone(text) → dict

# Output
{
  "summary": "...",
  "tone": "positif|négatif|neutre",
  "category": "...",
  "score": 0.XX
}
```

---

##  API Documentation

### Endpoints disponibles

| Méthode | Endpoint | Protection | Description |
|---------|----------|------------|-------------|
| `GET` | `/health` | ❌ Public | Health check de l'API |
| `POST` | `/register` | ❌ Public | Inscription utilisateur |
| `POST` | `/login` | ❌ Public | Connexion (génère JWT) |
| `POST` | `/analyse` | ✅ JWT | Analyse IA du texte |
| `GET` | `/test-env` | ❌ Public | Vérifier config (dev) |

---

###  GET /health

**Description :** Vérifier l'état de l'API

**Response 200 :**
```json
{
  "status": "ok",
  "message": "API opérationnelle"
}
```

---

###  POST /register

**Description :** Créer un nouveau compte utilisateur

**Request Body :**
```json
{
  "username": "john_doe",
  "password": "SecurePassword123!"
}
```

**Response 200 :**
```json
{
  "id": 1,
  "username": "john_doe",
  "created_at": "2025-12-12T10:30:00"
}
```

**Response 400 :** Utilisateur déjà existant
```json
{
  "detail": "Nom d'utilisateur déjà pris"
}
```

**Logique interne :**
```python
1. Vérifier si username existe déjà
2. Hasher le password (Argon2)
3. Créer User en BDD
4. Retourner user (sans password_hash)
```

---

###  POST /login

**Description :** Se connecter et obtenir un token JWT

**Request Body :**
```json
{
  "username": "john_doe",
  "password": "SecurePassword123!"
}
```

**Response 200 :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response 401 :** Identifiants incorrects
```json
{
  "detail": "Identifiants incorrects"
}
```

**Utilisation du token :**
```bash
curl -X POST http://localhost:8000/analyse \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Votre texte ici"}'
```

---

###  POST /analyse

**Description :** Analyser un texte avec orchestration IA

**Authentication :** Bearer Token (JWT) requis

**Request Headers :**
```
Authorization: Bearer <votre_token_jwt>
Content-Type: application/json
```

**Request Body :**
```json
{
  "text": "Apple Inc. a annoncé des résultats financiers record pour le trimestre, avec une augmentation de 15% du chiffre d'affaires. Les ventes d'iPhone ont dépassé les prévisions des analystes."
}
```

**Response 200 :**
```json
{
  "category": "Finance",
  "score": 0.9432,
  "summary": "Apple annonce des résultats trimestriels exceptionnels avec une hausse de 15% du CA et des ventes d'iPhone au-dessus des prévisions.",
  "tone": "positif"
}
```

**Response 401 :** Token invalide ou expiré
```json
{
  "detail": "Token invalide ou expiré"
}
```

**Workflow interne :**
```
1. Valider JWT token
2. Extraire username du token
3. Appeler classify_text() → (category, score)
4. Appeler summarize_and_analyze_tone() avec contexte
5. Agréger les résultats
6. Retourner JSON
```

---

###  GET /test-env

**Description :** Vérifier la configuration des API keys (développement uniquement)

**Response 200 :**
```json
{
  "hf_key_configured": true,
  "jwt_secret_configured": true,
  "hf_key_preview": "hf_aBcDeF..."
}
```

---

## Orchestration IA

### Service 1 : Classification Zero-Shot (Hugging Face)

#### Configuration
```python
# app/services/huggingface.py

MODEL = "facebook/bart-large-mnli"
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

CATEGORIES = [
    "Finance", "RH", "IT", "Opérations",
    "Marketing", "Juridique", "Sport", "Général"
]
```

#### Fonctionnement

**Zero-Shot Classification** : Le modèle peut classifier sans entraînement préalable sur des catégories spécifiques.

**Technique** : Natural Language Inference (NLI)
- Hypothèse : "Ce texte parle de Finance"
- Prémisse : Le texte analysé
- Résultat : Score de probabilité (0-1)

**Exemple de payload :**
```json
{
  "inputs": "Apple annonce ses résultats...",
  "parameters": {
    "candidate_labels": ["Finance", "RH", "IT", ...]
  }
}
```

**Exemple de réponse :**
```json
[
  {
    "label": "Finance",
    "score": 0.9432
  },
  {
    "label": "IT",
    "score": 0.0321
  },
  ...
]
```

---

### Service 2 : Synthèse Contextuelle (Google Gemini)

#### Configuration
```python
# app/services/gemini.py

MODEL = "gemini-2.5-flash"

config = types.GenerateContentConfig(
    system_instruction=f"Catégorie: {category}. Génère JSON...",
    response_mime_type="application/json",
    temperature=0.3  # Plus déterministe
)
```

#### Prompt Engineering

**Instruction système :**
```
Tu es un assistant d'analyse.
Génère uniquement du JSON avec deux champs :
- 'summary' (max 60 mots)
- 'tone' (positif|négatif|neutre)

Catégorie détectée : {category}
```

**Pourquoi la catégorie est importante ?**
- ✅ Contexte pour un résumé pertinent
- ✅ Vocabulaire adapté au domaine
- ✅ Cohérence entre classification et synthèse

**Exemple de prompt complet :**
```
User: "Apple Inc. a annoncé..."
System: "Catégorie: Finance. Génère JSON..."

→ Gemini comprend qu'il faut un résumé financier
```

#### Output structuré (JSON)

**Configuration :**
```python
response_mime_type="application/json"
```

**Exemple de réponse Gemini :**
```json
{
  "summary": "Apple annonce des résultats trimestriels exceptionnels avec une hausse de 15% du CA et des ventes d'iPhone au-dessus des prévisions.",
  "tone": "positif"
}
```

#### Analyse du ton

**Critères de détection :**
- **Positif** : Termes laudatifs, succès, croissance, record
- **Négatif** : Échec, baisse, critique, controverse
- **Neutre** : Factuel, sans jugement de valeur



---

### Flux d'orchestration complet

```python
# app/services/gemini.py

def summarize_and_analyze_tone(text):
    # ÉTAPE 1: Classification HF
    category, score = classify_text(text)
    
    # ÉTAPE 2: Préparation prompt contextualisé
    system_instruction = f"Catégorie: {category}. Génère JSON..."
    
    # ÉTAPE 3: Appel Gemini
    response = client.models.generate_content(
        model=MODEL,
        contents=[text],
        config=config
    )
    
    # ÉTAPE 4: Parsing JSON
    data = json.loads(response.text.strip())
    
    # ÉTAPE 5: Agrégation
    return {
        "summary": data["summary"],
        "tone": data["tone"],
        "category": category,
        "score": score
    }
```

---

##  Base de données

### Schéma PostgreSQL

#### Table `users`

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
```

**Modèle SQLAlchemy :**
```python
# app/models.py

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

```
**Frontend Repository** : [hybrid-analyzer-frontend](https://github.com/AyoubMotei/hybrid-analyzer-backend/tree/master)

---


**Dernière mise à jour** : Décembre 2025  
**Version** : 1.0.0  
**Auteur** : AYOUB MOTEI
