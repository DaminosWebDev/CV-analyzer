# CV-Analyzer-AI — Rapport de calibration des prompts

**Date** : 2026-03-25 10:18:01  
**Modèle** : llama-3.3-70b-versatile (Groq)  
**Combinaisons testées** : 9 (3 CVs × 3 offres)

## Résumé

| Prompt | Tests passés | Taux de réussite |
|--------|-------------|-----------------|
| Scoring | 9/9 | 100% |
| Keywords | 9/9 | 100% |

## Détail scoring

| CV | Offre | Score | Niveau | Durée | Statut |
|-----|-------|-------|--------|-------|--------|
| junior | fullstack | 22 | Faible correspondance | 1.2s | PASS |
| junior | ai_engineer | 18 | Inadapté | 1.0s | PASS |
| junior | devops | 12 | Inadapté | 0.9s | PASS |
| mid | fullstack | 87 | Très bon match | 1.4s | PASS |
| mid | ai_engineer | 42 | Correspondance partielle | 1.1s | PASS |
| mid | devops | 42 | Correspondance partielle | 1.2s | PASS |
| senior | fullstack | 60 | Correspondance partielle | 1.4s | PASS |
| senior | ai_engineer | 62 | Bon match | 2.2s | PASS |
| senior | devops | 82 | Très bon match | 4.3s | PASS |

## Détail keywords

| CV | Offre | Présentes | Manquantes | Statut |
|-----|-------|-----------|------------|--------|
| junior | fullstack | Python, HTML | FastAPI, Django, React, PostgreSQL, Dock | PASS |
| junior | ai_engineer | Python | LangChain, LlamaIndex, API OpenAI, API A | PASS |
| junior | devops | Python | Docker, Kubernetes, Terraform, AWS, GCP, | PASS |
| mid | fullstack | Python, FastAPI, React, PostgreSQL, Git | Django, Docker | PASS |
| mid | ai_engineer | Python, FastAPI | LangChain, LlamaIndex, API OpenAI, Anthr | PASS |
| mid | devops | Docker, Python, Git, AWS | Kubernetes, Terraform, GitHub Actions, G | PASS |
| senior | fullstack | Python, FastAPI, Django, React, PostgreS | Git, Docker | PASS |
| senior | ai_engineer | Python, FastAPI | LangChain, LlamaIndex, API OpenAI, Anthr | PASS |
| senior | devops | Docker, Kubernetes, Terraform, Python, G | AWS, GCP, Bash, Prometheus, Grafana, Git | PASS |

## Problèmes identifiés et corrections

Aucun problème détecté — tous les prompts passent la validation.

## Conclusion portfolio

Prompts testés sur 9 combinaisons CV/offre. Scoring : 9/9 tests passés. Keywords : 9/9 tests passés. JSON valide sur 100% des appels testés.