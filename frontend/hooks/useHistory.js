// frontend/hooks/useHistory.js
// Rôle : Logique de l'historique et du mode comparaison
// Dépendances : lib/storage.js, useState, useEffect

import { useState, useEffect, useCallback } from "react"
import {
  getHistory,
  saveToHistory,
  deleteFromHistory,
  clearHistory,
} from "@/lib/storage"

export function useHistory() {
  const [history, setHistory] = useState([])

  // Charger l'historique au premier rendu
  // useEffect avec [] = s'exécute une seule fois au montage du composant
  useEffect(() => {
    setHistory(getHistory())
  }, [])

  // ─────────────────────────────────────────────
  // Ajouter une analyse à l'historique
  // Appelé depuis useAnalyzer après une analyse réussie
  // ─────────────────────────────────────────────
  const addToHistory = useCallback((cvFileName, jobOfferPreview, results, advice) => {
    const entry = {
      cvFileName,
      // On garde juste les 100 premiers caractères de l'offre comme aperçu
      jobOfferPreview: jobOfferPreview.slice(0, 100) + "...",
      score: results.score,
      niveau: results.niveau,
      results,
      advice,
    }
    const updated = saveToHistory(entry)
    setHistory(updated)
  }, [])

  // ─────────────────────────────────────────────
  // Supprimer une entrée
  // ─────────────────────────────────────────────
  const removeFromHistory = useCallback((id) => {
    const updated = deleteFromHistory(id)
    setHistory(updated)
  }, [])

  // ─────────────────────────────────────────────
  // Vider tout l'historique
  // ─────────────────────────────────────────────
  const resetHistory = useCallback(() => {
    const updated = clearHistory()
    setHistory(updated)
  }, [])

  // ─────────────────────────────────────────────
  // Mode comparaison — sélection de 2 entrées max
  // ─────────────────────────────────────────────
  const [compareIds, setCompareIds] = useState([])

  const toggleCompare = useCallback((id) => {
    setCompareIds(prev => {
      // Si déjà sélectionné → on désélectionne
      if (prev.includes(id)) {
        return prev.filter(i => i !== id)
      }
      // Si déjà 2 sélectionnés → on remplace le plus ancien
      if (prev.length >= 2) {
        return [prev[1], id]
      }
      // Sinon → on ajoute
      return [...prev, id]
    })
  }, [])

  const clearCompare = useCallback(() => {
    setCompareIds([])
  }, [])

  // Les 2 entrées sélectionnées pour la comparaison
  const compareEntries = compareIds
    .map(id => history.find(e => e.id === id))
    .filter(Boolean) // Filtre les undefined si une entrée a été supprimée

  return {
    history,
    addToHistory,
    removeFromHistory,
    resetHistory,
    compareIds,
    toggleCompare,
    clearCompare,
    compareEntries,
  }
}