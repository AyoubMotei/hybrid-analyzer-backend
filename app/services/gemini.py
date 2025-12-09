from google import genai
from google.genai import types
import os, json
from dotenv import load_dotenv
from .huggingface import classify_text


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

def summarize_and_analyze_tone(text):
    category = classify_text(text)
  
   
    system_instruction = (
        f"Tu es un assistant d'analyse. "
        f"Génère uniquement du JSON avec deux champs : "
        f"'summary' (max 60 mots) et 'tone' (positif|négatif|neutre). "
        f"Catégorie: {category}."
    )

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        temperature=0.3
    )

    
    resp = client.models.generate_content(
        model=MODEL,
        contents=[text],
        config=config
    )

    text_response = resp.text.strip()

   
    
    data = json.loads(text_response)
      
    if "summary" in data and "tone" in data:
        return {
        "summary": data["summary"],
        "tone": data["tone"],
        "category": category[0],
        "score": category[1]
        }
        
        
    else:
            
        return {"summary": "Synthèse indisponible.", "tone": "neutre"}
   


if __name__ == "__main__":
    exemple = "I equipe marocaine est un bon equipe de football"
    result = summarize_and_analyze_tone(exemple)
    print(result)




