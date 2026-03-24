# backend/test_llm.py
# Test du service LLM — à supprimer après validation

from app.services.llm_service import call_llm, check_llm_connection

# Test 1 : vérification connexion
print("Test connexion Groq...")
result = check_llm_connection()
print(f"Status : {result['status']}")
print(f"Modèle : {result['model']}")
print(f"Réponse test : {result.get('test_response', result.get('error'))}")
print()

# Test 2 : appel simple
print("Test call_llm...")
response = call_llm(
    system_prompt="Tu es un assistant RH expert en recrutement. Réponds en français.",
    user_prompt="En une phrase, c'est quoi un CV parfait ?",
    max_tokens=100,
)
print(f"Réponse LLM : {response}")
print()
print("✅ Service LLM opérationnel !")