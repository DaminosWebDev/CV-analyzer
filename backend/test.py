# backend/test_groq.py
# Rôle       : Script de test — vérifie que la connexion Groq fonctionne
# Dépendances: groq, python-dotenv
# Usage      : python test_groq.py (depuis le dossier backend/, venv actif)

import os
from dotenv import load_dotenv
from groq import Groq

# ── Étape 1 : Charger les variables du fichier .env ──────────────────────────
load_dotenv()

# ── Étape 2 : Récupérer la clé API ───────────────────────────────────────────
api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Vérification de sécurité — on arrête tout si la clé est absente
if not api_key:
    print("❌ ERREUR : GROQ_API_KEY introuvable dans le fichier .env")
    print("   Vérifie que le fichier backend/.env existe et contient ta clé")
    exit(1)

print(f"✅ Clé API trouvée : {api_key[:8]}...{api_key[-4:]}")  # affiche début et fin seulement
print(f"✅ Modèle configuré : {model}")
print("─" * 50)

# ── Étape 3 : Créer le client Groq ───────────────────────────────────────────
client = Groq(api_key=api_key)

# ── Étape 4 : Envoyer un message test ────────────────────────────────────────
print("📤 Envoi du message à Groq...")

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "Tu es un assistant spécialisé dans l'analyse de CV. Réponds toujours en français."
        },
        {
            "role": "user",
            "content": "En une phrase, explique ce que tu peux faire pour aider quelqu'un à améliorer son CV."
        }
    ],
    max_tokens=150,  # limite la longueur de la réponse pour ce test
    temperature=0.7  # créativité modérée (0 = déterministe, 1 = très créatif)
)

# ── Étape 5 : Afficher la réponse ────────────────────────────────────────────
print("📥 Réponse de LLaMA 3.3 :")
print("─" * 50)
print(response.choices[0].message.content)
print("─" * 50)

# ── Étape 6 : Afficher les métadonnées utiles ────────────────────────────────
print(f"📊 Tokens utilisés : {response.usage.total_tokens}")
print(f"📊 Modèle utilisé  : {response.model}")
print("✅ Connexion Groq opérationnelle !")