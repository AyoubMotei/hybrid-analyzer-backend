from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chainage_complet(mocker):

    #  FAKE RÉPONSE GEMINI
    fake_gemini_result = {
        "summary": "Résumé simulé complet",
        "tone": "neutre",
        "category": "Sport",
        "score": 0.91
    }

    def fake_gemini(text):
        return fake_gemini_result

    #  PATCH DE LA FONCTION UTILISÉE
    mocker.patch(
        "app.main.summarize_and_analyze_tone",
        side_effect=fake_gemini
    )

    #  CRÉER UN USER
    client.post("/register", json={
        "username": "testuser",
        "password": "testpass"
    })

    #  LOGIN
    login = client.post("/login", json={
        "username": "testuser",
        "password": "testpass"
    })

    token = login.json()["access_token"]

    #  APPEL /analyse AVEC JSON BODY 
    headers = {"Authorization": f"Bearer {token}"}
    body = {"text": "Ceci est un test complet"}

    response = client.post("/analyse", json=body, headers=headers)

    #  ASSERTIONS
    assert response.status_code == 200

    data = response.json()
    assert data["summary"] == "Résumé simulé complet"
    assert data["tone"] == "neutre"
    assert data["category"] == "Sport"
    assert data["score"] == 0.91
