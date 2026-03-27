// frontend/lib/storage.js
// Rôle : Fonctions utilitaires pour lire/écrire l'historique dans localStorage
// Dépendances : aucune

const STORAGE_KEY = "cv_analyzer_history"
const MAX_ENTRIES = 10 // On garde les 10 dernières analyses

// ─────────────────────────────────────────────
// Lire tout l'historique
// Retourne : tableau d'entrées, ou [] si vide
// ─────────────────────────────────────────────
export function getHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    // Si rien en mémoire, on retourne un tableau vide
    return raw ? JSON.parse(raw) : []
  } catch {
    // JSON.parse peut planter si les données sont corrompues
    return []
  }
}

// ─────────────────────────────────────────────
// Sauvegarder une nouvelle analyse
// Reçoit : l'objet résultat complet
// Retourne : le nouvel historique complet
// ─────────────────────────────────────────────
export function saveToHistory(entry) {
  const history = getHistory()

  // Création de l'entrée avec métadonnées
  const newEntry = {
    id: Date.now().toString(), // ID unique basé sur le timestamp
    date: new Date().toISOString(),
    ...entry,
  }

  // On ajoute en tête de liste (plus récent en premier)
  const updated = [newEntry, ...history]

  // On limite à MAX_ENTRIES pour ne pas surcharger localStorage
  const trimmed = updated.slice(0, MAX_ENTRIES)

  localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmed))
  return trimmed
}

// ─────────────────────────────────────────────
// Supprimer une entrée par son ID
// ─────────────────────────────────────────────
export function deleteFromHistory(id) {
  const history = getHistory()
  const updated = history.filter(entry => entry.id !== id)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
  return updated
}

// ─────────────────────────────────────────────
// Vider tout l'historique
// ─────────────────────────────────────────────
export function clearHistory() {
  localStorage.removeItem(STORAGE_KEY)
  return []
}

// ─────────────────────────────────────────────
// Formater la date pour l'affichage
// Ex : "26 mars 2026 à 14h32"
// ─────────────────────────────────────────────
export function formatDate(isoString) {
  return new Date(isoString).toLocaleString("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}