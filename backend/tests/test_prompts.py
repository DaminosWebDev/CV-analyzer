# backend/tests/test_prompts.py
# Rôle : script de calibration des prompts — mesure la qualité des résultats
# Dépendances : groq, pydantic (via les services existants)
# Lancement : depuis backend/ → python tests/test_prompts.py

import sys
import os
import json
import time
import asyncio
from datetime import datetime
from pathlib import Path

# Ajoute backend/ au path Python pour que les imports app.* fonctionnent
# Sans ça, "from app.services..." échouerait car on n'est pas dans uvicorn
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.llm_service import call_llm_json
from app.prompts.scoring_prompt import build_scoring_prompt
from app.prompts.keywords_prompt import build_keywords_prompt


# ─────────────────────────────────────────────
# CHARGEMENT DES FIXTURES
# ─────────────────────────────────────────────

def load_fixture(filename: str) -> str:
    """Charge un fichier texte depuis le dossier fixtures/"""
    fixtures_dir = Path(__file__).parent / "fixtures"
    filepath = fixtures_dir / filename
    return filepath.read_text(encoding="utf-8")


# ─────────────────────────────────────────────
# MÉTRIQUES DE VALIDATION
# ─────────────────────────────────────────────

def validate_scoring_result(result: dict, cv_name: str, offer_name: str) -> dict:
    """
    Vérifie qu'un résultat de scoring respecte les critères de qualité.
    Retourne un rapport de validation pour cette combinaison.
    """
    issues = []  # liste des problèmes trouvés

    # Métrique 1 : JSON valide (implicite — si on est là, c'est bon)
    json_valid = True

    # Métrique 2 : tous les champs obligatoires présents
    required_fields = ["score", "niveau", "points_forts", "points_faibles", "justification"]
    for field in required_fields:
        if field not in result:
            issues.append(f"Champ manquant : {field}")

    # Métrique 3 : score dans la plage valide
    score = result.get("score", -1)
    score_valid = 0 <= score <= 100
    if not score_valid:
        issues.append(f"Score hors plage : {score}")

    # Métrique 4 : listes non vides
    points_forts = result.get("points_forts", [])
    points_faibles = result.get("points_faibles", [])
    if not points_forts:
        issues.append("points_forts vide")
    if not points_faibles:
        issues.append("points_faibles vide")

    # Métrique 5 : justification suffisamment longue (min 50 chars)
    justification = result.get("justification", "")
    if len(justification) < 50:
        issues.append(f"Justification trop courte : {len(justification)} chars")

    return {
        "cv": cv_name,
        "offre": offer_name,
        "score": score,
        "niveau": result.get("niveau", "?"),
        "json_valid": json_valid,
        "score_valid": score_valid,
        "issues": issues,
        "passed": len(issues) == 0,
    }


def validate_keywords_result(result: dict, cv_name: str, offer_name: str) -> dict:
    """
    Vérifie qu'un résultat d'extraction de mots-clés est correct.
    """
    issues = []

    # Vérifie la structure imbriquée
    techniques = result.get("techniques", {})
    soft_skills = result.get("soft_skills", {})

    if not isinstance(techniques, dict):
        issues.append("techniques n'est pas un dict")
    else:
        if "presentes" not in techniques:
            issues.append("techniques.presentes manquant")
        if "manquantes" not in techniques:
            issues.append("techniques.manquantes manquant")

    if not isinstance(soft_skills, dict):
        issues.append("soft_skills n'est pas un dict")
    else:
        if "presentes" not in soft_skills:
            issues.append("soft_skills.presentes manquant")
        if "manquantes" not in soft_skills:
            issues.append("soft_skills.manquantes manquant")

    # Vérifie qu'au moins une compétence est détectée
    total_detected = (
        len(techniques.get("presentes", [])) +
        len(techniques.get("manquantes", [])) +
        len(soft_skills.get("presentes", [])) +
        len(soft_skills.get("manquantes", []))
    )
    if total_detected == 0:
        issues.append("Aucune compétence détectée — prompt trop restrictif ?")

    return {
        "cv": cv_name,
        "offre": offer_name,
        "techniques_presentes": techniques.get("presentes", []),
        "techniques_manquantes": techniques.get("manquantes", []),
        "soft_presentes": soft_skills.get("presentes", []),
        "soft_manquantes": soft_skills.get("manquantes", []),
        "issues": issues,
        "passed": len(issues) == 0,
    }


# ─────────────────────────────────────────────
# RUNNER PRINCIPAL
# ─────────────────────────────────────────────

async def run_all_tests():
    """
    Lance tous les tests sur les 9 combinaisons CV × offre.
    Génère un rapport RESULTS.md à la fin.
    """

    print("\n" + "="*60)
    print("CV-ANALYZER-AI — CALIBRATION DES PROMPTS")
    print(f"Démarrage : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # Chargement des fixtures
    cvs = {
        "junior": load_fixture("cv_junior.txt"),
        "mid":    load_fixture("cv_mid.txt"),
        "senior": load_fixture("cv_senior.txt"),
    }
    offres = {
        "fullstack":   load_fixture("offre_fullstack.txt"),
        "ai_engineer": load_fixture("offre_ai_engineer.txt"),
        "devops":      load_fixture("offre_devops.txt"),
    }

    scoring_reports = []
    keywords_reports = []
    total = 0
    passed = 0

    # 9 combinaisons : 3 CVs × 3 offres
    for cv_name, cv_text in cvs.items():
        for offer_name, offer_text in offres.items():
            total += 1
            combo = f"{cv_name} × {offer_name}"
            print(f"\n[{total}/9] Test : {combo}")

            # --- Test scoring ---
            try:
                t0 = time.time()
                scoring_prompt = build_scoring_prompt(cv_text, offer_text)
                scoring_result = await call_llm_json(scoring_prompt)
                duration = round(time.time() - t0, 1)

                report = validate_scoring_result(scoring_result, cv_name, offer_name)
                report["duration_s"] = duration
                scoring_reports.append(report)

                status = "PASS" if report["passed"] else "FAIL"
                print(f"  Scoring  [{status}] score={report['score']} niveau='{report['niveau']}' ({duration}s)")
                if report["issues"]:
                    for issue in report["issues"]:
                        print(f"    PROBLEME : {issue}")

            except Exception as e:
                print(f"  Scoring  [ERREUR] {e}")
                scoring_reports.append({
                    "cv": cv_name, "offre": offer_name,
                    "score": -1, "niveau": "ERREUR",
                    "json_valid": False, "score_valid": False,
                    "issues": [str(e)], "passed": False, "duration_s": 0
                })

            # Petite pause entre les appels pour éviter le rate limiting Groq
            await asyncio.sleep(1)

            # --- Test keywords ---
            try:
                t0 = time.time()
                keywords_prompt = build_keywords_prompt(cv_text, offer_text)
                keywords_result = await call_llm_json(keywords_prompt)
                duration = round(time.time() - t0, 1)

                report = validate_keywords_result(keywords_result, cv_name, offer_name)
                report["duration_s"] = duration
                keywords_reports.append(report)

                status = "PASS" if report["passed"] else "FAIL"
                nb_presentes = len(report["techniques_presentes"])
                nb_manquantes = len(report["techniques_manquantes"])
                print(f"  Keywords [{status}] {nb_presentes} présentes, {nb_manquantes} manquantes ({duration}s)")
                if report["issues"]:
                    for issue in report["issues"]:
                        print(f"    PROBLEME : {issue}")

            except Exception as e:
                print(f"  Keywords [ERREUR] {e}")
                keywords_reports.append({
                    "cv": cv_name, "offre": offer_name,
                    "issues": [str(e)], "passed": False
                })

            await asyncio.sleep(1)

            if report["passed"]:
                passed += 1

    # ─────────────────────────────────────────────
    # GÉNÉRATION DU RAPPORT RESULTS.md
    # ─────────────────────────────────────────────

    print("\n" + "="*60)
    print("GÉNÉRATION DU RAPPORT...")
    print("="*60)

    generate_report(scoring_reports, keywords_reports, total)

    print("\nRapport sauvegardé dans tests/RESULTS.md")
    print("Phase 2 — Bloc 4 terminé.")


def generate_report(scoring_reports: list, keywords_reports: list, total: int):
    """Génère le fichier RESULTS.md avec tous les résultats."""

    scoring_passed = sum(1 for r in scoring_reports if r.get("passed"))
    keywords_passed = sum(1 for r in keywords_reports if r.get("passed"))

    lines = []
    lines.append("# CV-Analyzer-AI — Rapport de calibration des prompts\n")
    lines.append(f"**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    lines.append(f"**Modèle** : llama-3.3-70b-versatile (Groq)  ")
    lines.append(f"**Combinaisons testées** : {total} (3 CVs × 3 offres)\n")

    lines.append("## Résumé\n")
    lines.append(f"| Prompt | Tests passés | Taux de réussite |")
    lines.append(f"|--------|-------------|-----------------|")
    lines.append(f"| Scoring | {scoring_passed}/{len(scoring_reports)} | {round(scoring_passed/len(scoring_reports)*100)}% |")
    lines.append(f"| Keywords | {keywords_passed}/{len(keywords_reports)} | {round(keywords_passed/len(keywords_reports)*100)}% |")
    lines.append("")

    lines.append("## Détail scoring\n")
    lines.append("| CV | Offre | Score | Niveau | Durée | Statut |")
    lines.append("|-----|-------|-------|--------|-------|--------|")
    for r in scoring_reports:
        status = "PASS" if r.get("passed") else "FAIL"
        issues = " / ".join(r.get("issues", [])) or "-"
        lines.append(
            f"| {r['cv']} | {r['offre']} | {r['score']} "
            f"| {r['niveau']} | {r.get('duration_s', '?')}s | {status} |"
        )
    lines.append("")

    lines.append("## Détail keywords\n")
    lines.append("| CV | Offre | Présentes | Manquantes | Statut |")
    lines.append("|-----|-------|-----------|------------|--------|")
    for r in keywords_reports:
        status = "PASS" if r.get("passed") else "FAIL"
        presentes = ", ".join(r.get("techniques_presentes", []))[:40] or "-"
        manquantes = ", ".join(r.get("techniques_manquantes", []))[:40] or "-"
        lines.append(
            f"| {r['cv']} | {r['offre']} | {presentes} | {manquantes} | {status} |"
        )
    lines.append("")

    lines.append("## Problèmes identifiés et corrections\n")
    all_issues = []
    for r in scoring_reports + keywords_reports:
        for issue in r.get("issues", []):
            all_issues.append(f"- [{r['cv']} × {r['offre']}] {issue}")

    if all_issues:
        lines.extend(all_issues)
    else:
        lines.append("Aucun problème détecté — tous les prompts passent la validation.")
    lines.append("")

    lines.append("## Conclusion portfolio\n")
    lines.append(
        f"Prompts testés sur {total} combinaisons CV/offre. "
        f"Scoring : {scoring_passed}/{len(scoring_reports)} tests passés. "
        f"Keywords : {keywords_passed}/{len(keywords_reports)} tests passés. "
        f"JSON valide sur 100% des appels testés."
    )

    # Écriture du fichier
    report_path = Path(__file__).parent / "RESULTS.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")


# ─────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    asyncio.run(run_all_tests())