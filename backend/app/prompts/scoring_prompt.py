# backend/app/prompts/scoring_prompt.py
# Rôle : contient le prompt de scoring CV vs offre d'emploi
# Dépendances : aucune (fichier autonome, que du texte)

def build_scoring_prompt(cv_text: str, job_offer: str) -> str:
    """
    Construit le prompt complet pour scorer le match CV / offre.
    
    Technique utilisée : few-shot + format forcé JSON
    - Few-shot = on montre 2 exemples au LLM avant de lui donner la vraie tâche
    - Format forcé = on lui impose exactement la structure JSON à retourner
    
    Args:
        cv_text   : le texte brut du CV (extrait du PDF ou saisi manuellement)
        job_offer : le texte brut de l'offre d'emploi
    
    Returns:
        str : le prompt complet, prêt à être envoyé au LLM
    """

    # --- PARTIE 1 : le rôle du LLM ---
    # On lui dit qui il est et ce qu'on attend de lui.
    # "Expert RH" ancre son comportement sur le domaine RH plutôt que sur 
    # un domaine générique. C'est une technique simple mais efficace.
    system_context = """Tu es un expert RH et recruteur technique avec 10 ans d'expérience.
Tu analyses le match entre un CV et une offre d'emploi avec précision et objectivité.
Tu réponds UNIQUEMENT en JSON valide, sans texte avant, sans texte après, sans backticks."""

    # --- PARTIE 2 : les exemples few-shot ---
    # On montre au LLM 2 cas concrets AVANT de lui donner la vraie tâche.
    # Ça calibre son échelle de notation.
    # Remarque : les exemples sont volontairement simples pour être clairs.
    few_shot_examples = """
=== EXEMPLES DE RÉFÉRENCE ===

EXEMPLE 1 :
CV : "Étudiant en informatique, stage de 3 mois en Python basique, aucune expérience React"
Offre : "5 ans d'expérience React senior, TypeScript obligatoire, lead technique"
Réponse attendue :
{
  "score": 12,
  "niveau": "Inadapté",
  "points_forts": ["Notions Python"],
  "points_faibles": ["Aucune expérience React", "TypeScript manquant", "Niveau senior requis non atteint"],
  "justification": "Le profil junior ne correspond pas aux exigences senior de l'offre. Les technologies clés React et TypeScript sont absentes du CV."
}

EXEMPLE 2 :
CV : "3 ans développeur Python/FastAPI, projets React, connaissance Docker, anglais courant"
Offre : "Développeur Python 2-4 ans, FastAPI apprécié, React un plus, équipe internationale"
Réponse attendue :
{
  "score": 84,
  "niveau": "Très bon match",
  "points_forts": ["Python et FastAPI directement demandés", "React présent", "Anglais courant pour équipe internationale"],
  "points_faibles": ["Docker non mentionné dans l'offre", "Certifications non précisées"],
  "justification": "Le profil correspond précisément au poste. Les technologies principales sont maîtrisées et l'expérience est dans la fourchette demandée."
}

=== FIN DES EXEMPLES ===
"""

    # --- PARTIE 3 : l'échelle de notation ---
    # Sans ça, le LLM invente sa propre échelle. On la fixe explicitement.
    scoring_scale = """
ÉCHELLE DE SCORING OBLIGATOIRE :
- 0-20   : Profil inadapté (technologies totalement différentes, niveau très insuffisant)
- 21-40  : Faible correspondance (quelques points communs mais manques majeurs)
- 41-60  : Correspondance partielle (bases présentes, manques importants)
- 61-75  : Bon match (la plupart des critères remplis, quelques lacunes)
- 76-90  : Très bon match (profil bien adapté, lacunes mineures)
- 91-100 : Match quasi-parfait (profil idéal, dépasse les attentes)
"""

    # --- PARTIE 4 : la tâche réelle + format de sortie imposé ---
    # On impose la structure JSON exacte. Le LLM doit la respecter.
    # Chaque champ est décrit pour éviter les ambiguïtés.
    task = f"""
TÂCHE :
Analyse le match entre ce CV et cette offre d'emploi.

CV À ANALYSER :
{cv_text}

OFFRE D'EMPLOI :
{job_offer}

INSTRUCTIONS :
1. Applique l'échelle de scoring ci-dessus
2. Sois objectif et précis
3. Les points_forts et points_faibles doivent être SPÉCIFIQUES au CV et à l'offre donnés
4. La justification doit mentionner des éléments concrets des deux documents

FORMAT DE RÉPONSE OBLIGATOIRE (JSON brut uniquement) :
{{
  "score": <nombre entier entre 0 et 100>,
  "niveau": <"Inadapté" | "Faible match" | "Correspondance partielle" | "Bon match" | "Très bon match" | "Match quasi-parfait">,
  "points_forts": [<liste de strings, min 1, max 5>],
  "points_faibles": [<liste de strings, min 1, max 5>],
  "justification": <string de 2-3 phrases expliquant le score>
}}
"""

    # On assemble toutes les parties dans l'ordre logique
    return system_context + few_shot_examples + scoring_scale + task