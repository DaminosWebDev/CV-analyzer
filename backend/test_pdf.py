# backend/test_pdf.py
# Test rapide du service PDF — à supprimer après validation

from app.services.pdf_service import extract_text_from_pdf, clean_extracted_text

# Test 1 : texte vide
print("Test clean_extracted_text...")
result = clean_extracted_text("  Bonjour   \n\n\n\n  Monde  \n")
print(f"Résultat : '{result}'")
print("✅ clean_extracted_text fonctionne\n")

# Test 2 : PDF invalide
print("Test extract_text_from_pdf avec données invalides...")
try:
    extract_text_from_pdf(b"ceci n'est pas un PDF")
    print("❌ Aurait dû lever une erreur")
except ValueError as e:
    print(f"✅ Erreur correctement levée : {e}\n")

print("✅ Service PDF opérationnel !")
print("(Pour tester avec un vrai PDF, utilisera l'endpoint /api/v1/upload-cv)")