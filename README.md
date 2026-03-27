# CV Analyzer AI 🎯

> AI-powered tool that analyzes the compatibility between a resume and a job offer — instant score, missing keywords, and actionable improvement tips.

![Status](https://img.shields.io/badge/status-live-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![LLM](https://img.shields.io/badge/LLM-LLaMA_3.3_70b-blueviolet)
![License](https://img.shields.io/badge/license-MIT-blue)

**🔗 Live Demo:** `https://cv-analyzer-ai.vercel.app` ← *(replace after deployment)*

---

## 📸 Demo

> *Screenshot or GIF coming soon — add yours after deployment*

<!-- Once you have a demo GIF:
![CV Analyzer Demo](./docs/demo.gif)
-->

---

## ✨ Features

- **📄 CV Upload** — PDF or plain text, extracted on the fly with PyMuPDF
- **🎯 Match Score** — 0–100% compatibility score between the resume and job offer
- **🔑 Keyword Analysis** — identifies present and missing keywords
- **💡 Actionable Tips** — concrete improvement suggestions per CV section
- **⚡ Real-time Streaming** — AI response streamed via Server-Sent Events (SSE)
- **🕐 History** — last 10 analyses saved in localStorage, with comparison mode
- **🌙 Dark Mode** — professional dark UI, fully responsive
- **🔒 GDPR-friendly** — no data stored, stateless processing only

---

## 🛠️ Tech Stack

### Backend
| Technology | Role |
|---|---|
| **FastAPI** (Python) | Async REST API + SSE streaming |
| **Groq API** — LLaMA 3.3 70b | LLM inference (free tier) |
| **PyMuPDF** | PDF text extraction |
| **Pydantic v2** | Data validation & settings |

### Frontend
| Technology | Role |
|---|---|
| **Next.js 16** (App Router) | React framework |
| **Tailwind CSS v4** | Utility-first styling |
| **shadcn/ui 4.x** | UI component library |
| **JavaScript** | No TypeScript — intentional |

### Deployment
| Service | Layer | Cost |
|---|---|---|
| **Render.com** | Backend | Free |
| **Vercel** | Frontend | Free |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                   USER BROWSER                  │
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
│  GET  /analyze/advice (SSE stream)              │
└────────────────────┬────────────────────────────┘
                     │ API call
┌────────────────────▼────────────────────────────┐
│            Groq API — LLaMA 3.3 70b             │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repo

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

Create `backend/.env`:
```env
GROQ_API_KEY=gsk_your_key_here
ENVIRONMENT=development
```

Start the server:
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

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the dev server:
```bash
npm run dev
# → http://localhost:3000
```

---

## 📁 Project Structure

```
CV-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings & env vars (Pydantic)
│   │   ├── routers/
│   │   │   └── analyze.py       # API routes
│   │   ├── services/
│   │   │   ├── pdf_service.py   # PyMuPDF extraction
│   │   │   ├── llm_service.py   # Groq API client
│   │   │   └── analyze_service.py
│   │   ├── schemas/
│   │   │   └── analyze.py       # Pydantic models
│   │   └── prompts/             # LLM prompt templates
│   ├── render.yaml              # Render.com deployment config
│   └── requirements.txt
│
└── frontend/
    ├── app/
    │   ├── globals.css          # CSS variables + dark mode
    │   ├── layout.js
    │   └── page.js              # Single page, 2-column layout
    ├── components/
    │   └── cv-analyzer/         # Feature components
    ├── hooks/                   # useAnalyzer, useHistory
    └── lib/                     # api.js, storage.js, utils.js
```

---

## 🧠 How It Works

1. **User uploads** a CV (PDF or text) + pastes a job offer
2. **Backend extracts** text from PDF using PyMuPDF
3. **Three sequential LLM calls** via Groq API:
   - Scoring prompt → compatibility score (0–100)
   - Keywords prompt → present / missing keywords
   - Advice prompt → streamed improvement tips (SSE)
4. **Frontend displays** results in real time as tokens stream in
5. **Analysis saved** to localStorage for future comparison

---

## 🌐 Deployment

### Backend → Render.com

1. Connect your GitHub repo on [render.com](https://render.com)
2. Set **Root Directory** to `backend`
3. **Build command:** `pip install -r requirements.txt`
4. **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GROQ_API_KEY`

### Frontend → Vercel

1. Import your repo on [vercel.com](https://vercel.com)
2. Set **Root Directory** to `frontend`
3. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-render-url.onrender.com`

---

## 🔮 Roadmap

- [ ] Multi-language support (EN/FR)
- [ ] Export analysis as PDF report
- [ ] LinkedIn job offer URL auto-import
- [ ] Cover letter generator based on analysis

---

## 👤 Author

**DaminosWebDev**
- GitHub: [@DaminosWebDev](https://github.com/DaminosWebDev)

---

## 📄 License

MIT — free to use, fork, and learn from.