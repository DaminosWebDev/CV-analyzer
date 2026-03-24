# backend/test_analyze.py
# Test du service analyse — à supprimer après validation

from app.services.analyze_service import analyze_cv

# CV et offre d'exemple
cv_text = """
Jean Dupont - Développeur Full-Stack
Email: jean.dupont@email.com

EXPÉRIENCE
- 3 ans chez TechCorp : développement Python/FastAPI, APIs REST
- 2 ans chez StartupXYZ : React, JavaScript, Node.js

COMPÉTENCES
Python, FastAPI, React, JavaScript, Git, Docker, PostgreSQL

FORMATION
Master Informatique - Université Paris 6 - 2019
"""

job_offer = """
Nous recherchons un Développeur Full-Stack Python/React (H/F)

MISSIONS :
- Développer des APIs REST avec FastAPI
- Créer des interfaces React modernes
- Travailler en équipe Agile/Scrum
- Déployer sur AWS

COMPÉTENCES REQUISES :
- Python (FastAPI ou Django)
- React.js
- SQL (PostgreSQL ou MySQL)
- Docker
- Git

COMPÉTENCES SOUHAITÉES :
- AWS ou GCP
- TypeScript
- Tests unitaires (pytest)
"""

print("🔄 Analyse en cours... (10-15 secondes)")
result = analyze_cv(cv_text, job_offer)

print(f"\n📊 Score : {result.match_score}/100 ({result.match_level})")
print(f"\n✅ Mots-clés présents : {result.keywords.present}")
print(f"❌ Mots-clés manquants : {result.keywords.missing}")
print(f"⭐ Bonus : {result.keywords.bonus}")
print(f"\n💡 Top recommandations :")
for i, rec in enumerate(result.top_recommendations, 1):
    print(f"  {i}. {rec}")
print("\n✅ Service Analyse opérationnel !")