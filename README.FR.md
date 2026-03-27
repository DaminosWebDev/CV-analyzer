# CV Analyzer AI 🎯

> Outil IA qui analyse la compatibilité entre un CV et une offre d'emploi — score instantané, mots-clés manquants et conseils concrets d'amélioration.

![Status](https://img.shields.io/badge/statut-en_ligne-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![LLM](https://img.shields.io/badge/LLM-LLaMA_3.3_70b-blueviolet)
![License](https://img.shields.io/badge/licence-MIT-blue)

**🔗 Démo en ligne :** `https://cv-analyzer-ai.vercel.app` ← *(à remplacer après déploiement)*

---

## 📸 Démonstration

> *Capture d'écran ou GIF à venir — à ajouter après déploiement*

<!-- Une fois le GIF de démo prêt :
![Démonstration CV Analyzer](./docs/demo.gif)
-->

---

## ✨ Fonctionnalités

- **📄 Upload CV** — PDF ou texte brut, extraction à la volée avec PyMuPDF
- **🎯 Score de match** — compatibilité 0–100% entre le CV et l'offre
- **🔑 Analyse des mots-clés** — identifie les mots-clés présents et manquants
- **💡 Conseils actionnables** — suggestions d'amélioration concrètes par section du CV
- **⚡ Streaming temps réel** — réponse IA streamée via Server-Sent Events (SSE)
- **🕐 Historique** — 10 dernières analyses sauvegardées en localStorage, avec mode comparaison
- **🌙 Mode sombre** — UI dark professionnelle, entièrement responsive
- **🔒 RGPD-friendly** — aucune donnée stockée, traitement stateless uniquement

---

## 🛠️ Stack technique

### Backend
| Technologie | Rôle |
|---|---|
| **FastAPI** (Python) | API REST async + streaming SSE |
| **Groq API** — LLaMA 3.3 70b | Inférence LLM (plan gratuit) |
| **PyMuPDF** | Extraction texte depuis PDF |
| **Pydantic v2** | Validation des données & configuration |

### Frontend
| Technologie | Rôle |
|---|---|
| **Next.js 16** (App Router) | Framework React |
| **Tailwind CSS v4** | Styles utilitaires |
| **shadcn/ui 4.x** | Bibliothèque de composants UI |
| **JavaScript** | Sans TypeScript — choix délibéré |

### Déploiement
| Service | Couche | Coût |
|---|---|---|
| **Render.com** | Backend | Gratuit |
| **Vercel** | Frontend | Gratuit |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│               NAVIGATEUR UTILISATEUR            │
│  Next.js 16 (Vercel)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │CVUploader│  │ScoreCard │  │ AdviceStream │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────┘
                     │ HTTP / SSE
┌────────────────────▼────────────────────────────┐
│              FastAPI (Render.com)               │
│  POST /analyze/upload-cv                        │
│  POST /analyze/score                            │
│  POST /analyze/keywords                         │
│  GET  /analyze/advice (stream SSE)              │
└────────────────────┬────────────────────────────┘
                     │ Appel API
┌────────────────────▼────────────────────────────┐
│            Groq API — LLaMA 3.3 70b             │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Installation locale

### Prérequis
- Python 3.11+
- Node.js 18+
- Une [clé API Groq](https://console.groq.com) gratuite

### 1. Cloner le repo

```bash
git clone https://github.com/DaminosWebDev/CV-analyzer.git
cd CV-analyzer
```

### 2. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Créer `backend/.env` :
```env
GROQ_API_KEY=gsk_ta_cle_ici
ENVIRONMENT=development
```

Lancer le serveur :
```bash
uvicorn app.main:app --reload
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

### 3. Frontend

```bash
cd frontend
npm install
```

Créer `frontend/.env.local` :
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Lancer le serveur de dev :
```bash
npm run dev
# → http://localhost:3000
```

---

## 📁 Structure du projet

```
CV-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py              # Point d'entrée FastAPI
│   │   ├── config.py            # Configuration & variables d'env (Pydantic)
│   │   ├── routers/
│   │   │   └── analyze.py       # Routes API
│   │   ├── services/
│   │   │   ├── pdf_service.py   # Extraction PyMuPDF
│   │   │   ├── llm_service.py   # Client Groq API
│   │   │   └── analyze_service.py
│   │   ├── schemas/
│   │   │   └── analyze.py       # Modèles Pydantic
│   │   └── prompts/             # Templates de prompts LLM
│   ├── render.yaml              # Config déploiement Render.com
│   └── requirements.txt
│
└── frontend/
    ├── app/
    │   ├── globals.css          # Variables CSS + dark mode
    │   ├── layout.js
    │   └── page.js              # Page unique, layout 2 colonnes
    ├── components/
    │   └── cv-analyzer/         # Composants métier
    ├── hooks/                   # useAnalyzer, useHistory
    └── lib/                     # api.js, storage.js, utils.js
```

---

## 🧠 Comment ça fonctionne

1. **L'utilisateur upload** son CV (PDF ou texte) + colle une offre d'emploi
2. **Le backend extrait** le texte du PDF via PyMuPDF
3. **Trois appels LLM séquentiels** via Groq API :
   - Prompt scoring → score de compatibilité (0–100)
   - Prompt keywords → mots-clés présents / manquants
   - Prompt conseils → conseils streamés en SSE
4. **Le frontend affiche** les résultats en temps réel au fil du streaming
5. **L'analyse est sauvegardée** en localStorage pour comparaison future

---

## 🌐 Déploiement

### Backend → Render.com

1. Connecter ton repo GitHub sur [render.com](https://render.com)
2. Définir **Root Directory** : `backend`
3. **Build command :** `pip install -r requirements.txt`
4. **Start command :** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Ajouter la variable d'environnement : `GROQ_API_KEY`

### Frontend → Vercel

1. Importer ton repo sur [vercel.com](https://vercel.com)
2. Définir **Root Directory** : `frontend`
3. Ajouter la variable d'environnement : `NEXT_PUBLIC_API_URL=https://ton-url-render.onrender.com`

---

## 🔮 Roadmap

- [ ] Support multilingue (FR/EN)
- [ ] Export de l'analyse en rapport PDF
- [ ] Import automatique depuis une URL LinkedIn
- [ ] Génération de lettre de motivation basée sur l'analyse

---

## 👤 Auteur

**DaminosWebDev**
- GitHub : [@DaminosWebDev](https://github.com/DaminosWebDev)

---

## 📄 Licence

MIT — libre d'utilisation, de fork et d'apprentissage.