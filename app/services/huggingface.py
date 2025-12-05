import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")


API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"


CATEGORIES = ["refund", "legal", "faq", "AI", "Finance", "RH", "Opérations", "Juridique", "Marketing", "Général", "Sport"]

def classify_text(text):

    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": CATEGORIES}
    }

   
    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()

    
    label = data[0]["label"]
    score = data[0]["score"]

    return label, score



if __name__ == "__main__":
    result = classify_text("Il s'agit du meilleur modèle au monde pour la compréhension multimodale.")
    print(result)
