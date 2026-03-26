# backend/app/services/llm_service.py
# Rôle : communication avec l'API Groq (LLM)
# Dépendances : groq, config.py
# MODIFICATION : ajout de call_llm_json() et clean_json_response()

import json
import re
from groq import Groq
from app.config import settings

# Client Groq initialisé une seule fois au démarrage
# (pas besoin d'en créer un nouveau à chaque appel)
client = Groq(api_key=settings.groq_api_key)


def clean_json_response(text: str) -> str:
    """
    Nettoie la réponse du LLM pour extraire uniquement le JSON valide.
    
    Problème courant : le LLM retourne parfois :
      "Bien sûr ! Voici le résultat : ```json { ... } ``` "
    Au lieu de simplement :
      { ... }
    
    Cette fonction extrait le JSON propre dans les deux cas.
    
    Args:
        text : la réponse brute du LLM
    
    Returns:
        str : le JSON nettoyé, prêt pour json.loads()
    """
    # Étape 1 : supprimer les espaces/sauts de ligne en début et fin
    text = text.strip()
    
    # Étape 2 : chercher un bloc ```json ... ``` (cas le plus fréquent)
    # re.DOTALL = le "." matche aussi les sauts de ligne
    json_block = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if json_block:
        return json_block.group(1).strip()
    
    # Étape 3 : chercher un bloc ``` ... ``` sans "json"
    code_block = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if code_block:
        return code_block.group(1).strip()
    
    # Étape 4 : chercher directement { ... } dans la réponse
    # Utile si le LLM écrit du texte AVANT le JSON
    brace_match = re.search(r'\{.*\}', text, re.DOTALL)
    if brace_match:
        return brace_match.group(0).strip()
    
    # Étape 5 : rien trouvé → on retourne le texte tel quel
    # L'appelant devra gérer l'exception json.loads()
    return text


async def call_llm_json(prompt: str) -> dict:
    """
    Envoie un prompt au LLM et retourne la réponse parsée en dict Python.
    
    Contrairement à call_llm() qui retourne du texte brut,
    call_llm_json() s'attend à recevoir du JSON et le parse automatiquement.
    
    Args:
        prompt : le prompt complet (construit par build_scoring_prompt, etc.)
    
    Returns:
        dict : la réponse du LLM parsée en dictionnaire Python
    
    Raises:
        ValueError : si le LLM ne retourne pas du JSON valide après nettoyage
    """
    try:
        # Appel à l'API Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,  # Très bas : on veut des réponses reproductibles
                               # 0.0 = déterministe, 1.0 = très créatif
                               # Pour du JSON structuré → toujours proche de 0
            max_tokens=1000,   # Le JSON de scoring est petit, 1000 tokens suffisent
        )
        
        # Extraction du texte de la réponse
        raw_text = response.choices[0].message.content
        
        # Nettoyage du JSON parasite
        clean_text = clean_json_response(raw_text)
        
        # Parsing JSON → dict Python
        # Si ça plante ici, c'est que le prompt doit être amélioré
        result = json.loads(clean_text)
        
        return result
        
    except json.JSONDecodeError as e:
        # Le LLM n'a pas retourné du JSON valide
        # On lève une erreur claire avec le texte brut pour déboguer
        raise ValueError(
            f"Le LLM n'a pas retourné du JSON valide.\n"
            f"Erreur : {e}\n"
            f"Réponse brute reçue : {raw_text[:500]}"  # On tronque à 500 chars
        )
    
    except Exception as e:
        # Erreur API Groq (quota, connexion, etc.)
        raise ValueError(f"Erreur lors de l'appel au LLM : {e}")


# --- Garde la fonction existante pour le streaming (Bloc 3) ---
async def call_llm_stream(prompt: str):
    """
    Envoie un prompt au LLM et retourne les tokens un par un via un générateur async.

    Contrairement à call_llm_json() qui attend la réponse complète,
    call_llm_stream() yield chaque morceau de texte dès qu'il arrive.

    C'est un "générateur async" — il utilise "yield" au lieu de "return".
    Chaque "yield" envoie un token au code appelant sans fermer la fonction.

    Args:
        prompt : le prompt complet à envoyer

    Yields:
        str : chaque token de texte généré par le LLM
    """
    try:
        # stream=True → Groq envoie les tokens au fur et à mesure
        # au lieu d'attendre que tout soit généré
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,  # Plus élevé qu'au Bloc 1 : on veut des conseils
                               # variés et naturels, pas des réponses robotiques
            max_tokens=800,    # ~350 mots — cohérent avec la consigne du prompt
            stream=True,       # ← LA CLÉ : active le streaming token par token
        )

        # On itère sur les chunks reçus au fur et à mesure
        for chunk in response:
            # Chaque chunk contient potentiellement un morceau de texte
            # On vérifie qu'il n'est pas vide avant de le yielder
            token = chunk.choices[0].delta.content
            if token is not None:
                yield token

    except Exception as e:
        # En cas d'erreur, on yield un message d'erreur formaté
        # Le frontend pourra le détecter et l'afficher
        yield f"[ERREUR] {str(e)}"