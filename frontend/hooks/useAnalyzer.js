// frontend/hooks/useAnalyzer.js
// Rôle : Logique métier centralisée — état et actions de l'analyseur
// Dépendances : lib/api.js, hooks React (useState, useCallback)

import { useState, useCallback } from "react"
import { uploadCV, analyzeCV, streamAdvice } from "@/lib/api"

// ─────────────────────────────────────────────
// ÉTAT INITIAL — toutes les données de l'app
// ─────────────────────────────────────────────
const initialState = {
  // Étape courante du flux utilisateur
  step: "input",        // "input" | "loading" | "results"

  // Données d'entrée
  cvFile: null,         // l'objet File du PDF uploadé
  cvText: "",           // le texte extrait du PDF par le backend
  jobOffer: "",         // le texte de l'offre d'emploi saisi

  // Résultats de l'analyse
  results: null,        // { score, niveau, points_forts, points_faibles, justification, keywords }

  // Streaming des conseils
  advice: "",           // texte des conseils qui s'accumule token par token
  isStreaming: false,   // true pendant que les conseils arrivent

  // Gestion des erreurs
  error: null,          // message d'erreur à afficher
}

export function useAnalyzer() {
  const [state, setState] = useState(initialState)

  // Helper pour mettre à jour une seule clé de l'état
  // Analogie : comme modifier une seule case d'un formulaire
  const update = useCallback((patch) => {
    setState(prev => ({ ...prev, ...patch }))
  }, [])

  // ─────────────────────────────────────────────
  // ACTION 1 : L'utilisateur sélectionne un fichier PDF
  // ─────────────────────────────────────────────
  const handleFileSelect = useCallback(async (file) => {
  console.log("🔍 handleFileSelect appelé avec :", file)

  if (!file) {
    console.log("❌ Pas de fichier")
    return
  }
  if (file.type !== "application/pdf") {
    console.log("❌ Type invalide :", file.type)
    update({ error: "Seuls les fichiers PDF sont acceptés." })
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    console.log("❌ Fichier trop grand :", file.size)
    update({ error: "Le fichier est trop volumineux (5 Mo maximum)." })
    return
  }

  console.log("✅ Fichier valide, upload en cours...")
  update({ cvFile: file, error: null })

  try {
    const data = await uploadCV(file)
    console.log("✅ Réponse backend :", data)
    update({ cvText: data.text })
  } catch (err) {
    console.log("❌ Erreur upload :", err.message)
    update({ error: err.message })
  }
}, [update])

  // ─────────────────────────────────────────────
  // ACTION 2 : L'utilisateur modifie l'offre d'emploi
  // ─────────────────────────────────────────────
  const handleJobOfferChange = useCallback((text) => {
    update({ jobOffer: text, error: null })
  }, [update])

  // ─────────────────────────────────────────────
  // ACTION 3 : Lancement de l'analyse complète
  // ─────────────────────────────────────────────
  const handleAnalyze = useCallback(async () => {
    // Validations avant d'appeler le backend
    if (!state.cvText) {
      update({ error: "Veuillez d'abord uploader votre CV." })
      return
    }
    if (!state.jobOffer.trim()) {
      update({ error: "Veuillez coller une offre d'emploi." })
      return
    }
    if (state.jobOffer.trim().length < 50) {
      update({ error: "L'offre d'emploi semble trop courte (50 caractères minimum)." })
      return
    }

    // Phase 1 : Analyse JSON (score + keywords)
    update({ step: "loading", error: null, results: null, advice: "" })

    try {
      const data = await analyzeCV(state.cvText, state.jobOffer)

      // On stocke les résultats et on passe à l'affichage
      update({ results: data.data, step: "results" })

      // Phase 2 : Streaming des conseils (en parallèle de l'affichage)
      update({ isStreaming: true })

      const stream = await streamAdvice(
        state.cvText,
        state.jobOffer,
        data.data.score,
        data.data.points_faibles
      )

      // Lecture du stream token par token
      // TextDecoder convertit les bytes en texte lisible
      const reader = stream.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        // Chaque chunk peut contenir plusieurs lignes SSE
        const chunk = decoder.decode(value)
        const lines = chunk.split("\n")

        for (const line of lines) {
  if (line.startsWith("data: ")) {
    const raw = line.slice(6) // → '{"token": "##"}'

    // Ignore le signal de fin de stream
    if (raw === "[DONE]") continue

    try {
      const parsed = JSON.parse(raw)       // → { token: "##" }
      const tokenText = parsed.token ?? "" // → "##"
      if (tokenText) {
        setState(prev => ({ ...prev, advice: prev.advice + tokenText }))
      }
    } catch {
      // Ligne malformée — on l'ignore silencieusement
    }
  }
        }
      }

    } catch (err) {
      update({ error: err.message, step: "input" })
    } finally {
      update({ isStreaming: false })
    }
  }, [state.cvText, state.jobOffer, update])

  // ─────────────────────────────────────────────
  // ACTION 4 : Recommencer une nouvelle analyse
  // ─────────────────────────────────────────────
  const handleReset = useCallback(() => {
    setState(initialState)
  }, [])

  // On expose l'état et les actions aux composants
  return {
    ...state,
    handleFileSelect,
    handleJobOfferChange,
    handleAnalyze,
    handleReset,
  }
}