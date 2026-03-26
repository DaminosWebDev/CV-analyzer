# backend/app/prompts/keywords_prompt.py
# Rôle : prompt d'extraction des mots-clés techniques et soft skills
# Dépendances : aucune

def build_keywords_prompt(cv_text: str, job_offer: str) -> str:
    """
    Construit le prompt pour extraire les compétences présentes et manquantes.

    Règle clé : le LLM ne peut citer que des éléments PRÉSENTS dans les textes.
    Il ne doit pas inventer de compétences non mentionnées.

    Args:
        cv_text   : texte brut du CV
        job_offer : texte brut de l'offre d'emploi

    Returns:
        str : le prompt complet prêt à envoyer au LLM
    """

    system_context = """Tu es un expert en recrutement technique.
Tu extrais avec précision les compétences d'un CV et d'une offre d'emploi.
RÈGLE ABSOLUE : tu ne cites QUE des éléments explicitement présents dans les textes fournis.
Tu ne dois JAMAIS inventer ou suggérer des compétences non mentionnées.
Tu réponds UNIQUEMENT en JSON valide, sans texte avant, sans texte après, sans backticks."""

    few_shot_examples = """
=== EXEMPLES DE RÉFÉRENCE ===

EXEMPLE 1 :
CV : "3 ans Python, Django, PostgreSQL, tests unitaires pytest, Git, anglais B2"
Offre : "Python senior, FastAPI ou Django, SQL obligatoire, Docker apprécié, anglais courant"
Réponse attendue :
{
  "techniques": {
    "presentes": ["Python", "Django", "PostgreSQL", "Git"],
    "manquantes": ["FastAPI", "Docker"]
  },
  "soft_skills": {
    "presentes": ["Anglais B2"],
    "manquantes": ["Anglais courant (niveau non précisé comme courant)"]
  }
}

EXEMPLE 2 :
CV : "Développeur React/TypeScript 4 ans, Redux, REST APIs, méthodes agiles, leadership équipe"
Offre : "Frontend React, TypeScript, GraphQL obligatoire, esprit d'équipe, autonomie"
Réponse attendue :
{
  "techniques": {
    "presentes": ["React", "TypeScript", "REST APIs"],
    "manquantes": ["GraphQL"]
  },
  "soft_skills": {
    "presentes": ["Méthodes agiles", "Leadership équipe"],
    "manquantes": ["Autonomie (non mentionnée explicitement)"]
  }
}

=== FIN DES EXEMPLES ===
"""

    instructions = """
INSTRUCTIONS STRICTES :
1. "presentes" = compétences demandées dans l'offre ET présentes dans le CV
2. "manquantes" = compétences demandées dans l'offre MAIS absentes du CV
3. N'inclus PAS les compétences du CV qui ne sont pas demandées dans l'offre
4. Sois précis sur les noms : "FastAPI" pas "framework Python", "Docker" pas "containerisation"
5. Limite à 8 éléments maximum par liste pour rester lisible
6. Pour les soft skills : cherche communication, leadership, autonomie, 
   travail en équipe, langues, méthodes de travail (agile, scrum...)
"""

    task = f"""
TÂCHE :
Analyse ces deux documents et extrais les compétences.

CV :
{cv_text}

OFFRE D'EMPLOI :
{job_offer}

FORMAT DE RÉPONSE OBLIGATOIRE (JSON brut uniquement) :
{{
  "techniques": {{
    "presentes": [<liste de strings — compétences techniques matchées>],
    "manquantes": [<liste de strings — compétences techniques absentes du CV>]
  }},
  "soft_skills": {{
    "presentes": [<liste de strings — soft skills matchés>],
    "manquantes": [<liste de strings — soft skills absents du CV>]
  }}
}}
"""

    return system_context + few_shot_examples + instructions + task