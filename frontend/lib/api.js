// frontend/lib/api.js
// Rôle : Toutes les fonctions d'appel vers le backend FastAPI
// Dépendances : variable d'environnement NEXT_PUBLIC_API_URL

// Récupère l'URL du backend depuis .env.local
// En dev : http://localhost:8000
// En prod : l'URL Render.com (on configurera ça au déploiement)
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// ─────────────────────────────────────────────
// FONCTION 1 : Upload d'un CV en PDF
// Reçoit : un objet File (le fichier PDF sélectionné)
// Retourne : { success: true, cv_text: "..." } ou lance une erreur
// ─────────────────────────────────────────────
export async function uploadCV(file) {
  // FormData = la façon standard d'envoyer un fichier via HTTP
  const formData = new FormData()
  formData.append("file", file)

  const response = await fetch(`${API_URL}/api/v1/upload-cv`, {
    method: "POST",
    body: formData,
    // NB : ne pas mettre Content-Type manuellement avec FormData
    // le navigateur le fait automatiquement avec le bon "boundary"
  })

  // Si le serveur répond avec une erreur HTTP (400, 500, etc.)
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Erreur lors de l'upload du CV")
  }

  return response.json()
}

// ─────────────────────────────────────────────
// FONCTION 2 : Analyser CV + offre d'emploi
// Reçoit : { cv_text, job_offer }
// Retourne : { success: true, data: { score, niveau, keywords, ... } }
// ─────────────────────────────────────────────
export async function analyzeCV(cvText, jobOffer) {
  const response = await fetch(`${API_URL}/api/v1/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      cv_text: cvText,
      job_offer: jobOffer,
    }),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Erreur lors de l'analyse")
  }

  return response.json()
}

// ─────────────────────────────────────────────
// FONCTION 3 : Streaming des conseils (SSE)
// Reçoit : { cv_text, job_offer, score, points_faibles }
// Retourne : un ReadableStream (flux de tokens)
// NB : cette fonction est différente — elle ne retourne pas du JSON
//      mais un flux de texte token par token
// ─────────────────────────────────────────────
export async function streamAdvice(cvText, jobOffer, score, pointsFaibles) {
  const response = await fetch(`${API_URL}/api/v1/analyze/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      cv_text: cvText,
      job_offer: jobOffer,
      score: score,
      points_faibles: pointsFaibles,
    }),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || "Erreur lors du streaming")
  }

  // On retourne le body brut — c'est un ReadableStream
  // On le lira token par token dans useAnalyzer.js
  return response.body
}