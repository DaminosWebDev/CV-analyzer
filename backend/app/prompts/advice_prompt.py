# backend/app/prompts/advice_prompt.py
# Rôle : prompt de génération des conseils d'amélioration du CV
# Dépendances : aucune


def build_advice_prompt(
    cv_text: str,
    job_offer: str,
    score: int,
    points_faibles: list,
) -> str:
    """
    Construit le prompt pour générer des conseils d'amélioration concrets.

    Ce prompt est différent des deux premiers :
    - Il reçoit en plus le score et les points_faibles déjà calculés (Bloc 1)
    - Il génère du TEXTE libre (pas du JSON) — donc pas de format forcé
    - Il est conçu pour le streaming token par token

    Args:
        cv_text       : texte brut du CV
        job_offer     : texte brut de l'offre d'emploi
        score         : score calculé au Bloc 1 (ex: 82)
        points_faibles: liste des points faibles calculés au Bloc 1

    Returns:
        str : le prompt complet prêt à streamer
    """

    # On formate les points faibles en liste à puces lisible pour le LLM
    # ["Manque Docker", "React basique"] → "- Manque Docker\n- React basique"
    points_faibles_str = "\n".join(f"- {point}" for point in points_faibles)

    # Si pas de points faibles (score parfait), on met un message par défaut
    if not points_faibles_str:
        points_faibles_str = "- Aucun point faible majeur identifié"

    system_context = """Tu es un coach carrière expert en recrutement tech.
Tu donnes des conseils CONCRETS et ACTIONNABLES pour améliorer un CV.
Tes conseils sont directs, bienveillants et immédiatement applicables.
Tu t'exprimes en français, avec un ton professionnel mais accessible."""

    # On donne au LLM le contexte déjà calculé par les Blocs 1 et 2
    # Ça évite de recalculer et rend les conseils plus cohérents
    context = f"""
CONTEXTE DE L'ANALYSE :
- Score de match actuel : {score}/100
- Points à améliorer identifiés :
{points_faibles_str}
"""

    task = f"""
CV DU CANDIDAT :
{cv_text}

OFFRE D'EMPLOI CIBLÉE :
{job_offer}

MISSION :
Génère des conseils d'amélioration structurés en 3 sections :

## 1. Compétences à mettre en avant
Identifie les compétences du CV qui correspondent à l'offre mais sont
mal formulées ou sous-valorisées. Donne des formulations concrètes.

## 2. Lacunes à combler
Pour chaque point faible identifié, propose une action concrète :
formation, projet personnel, certification, ou reformulation.

## 3. Améliorations de forme
Donne 2-3 conseils sur la structure et la présentation du CV
pour maximiser l'impact sur ce type de poste.

RÈGLES :
- Chaque conseil doit être SPÉCIFIQUE à ce CV et cette offre
- Pas de conseils génériques comme "améliorez vos compétences"
- Mentionne des technologies, outils ou formulations précises
- Longueur totale : 250-350 mots
"""

    return system_context + context + task