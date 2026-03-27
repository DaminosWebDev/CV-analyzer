// frontend/components/cv-analyzer/HistoryPanel.js
// Rôle : Liste des analyses passées avec actions (revoir, comparer, supprimer)
// Dépendances : shadcn/ui Card Badge Button, lib/storage formatDate

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { formatDate } from "@/lib/storage"

// Couleur du score — même logique que ScoreCard
function getScoreColor(score) {
  if (score >= 70) return "text-green-600"
  if (score >= 40) return "text-orange-500"
  return "text-red-500"
}

// Sous-composant pour une entrée d'historique
function HistoryEntry({ entry, isSelectedForCompare, onCompare, onDelete, onView }) {
  return (
    <div className={`
      p-3 rounded-lg border transition-colors
      ${isSelectedForCompare
        ? "border-blue-400 bg-blue-50"
        : "border-slate-200 bg-white hover:border-slate-300"
      }
    `}>
      <div className="flex items-start justify-between gap-2">

        {/* Infos principales */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            {/* Score */}
            <span className={`text-xl font-bold ${getScoreColor(entry.score)}`}>
              {entry.score}/100
            </span>
            {/* Niveau */}
            <Badge variant="outline" className="text-xs">
              {entry.niveau}
            </Badge>
            {/* Indicateur comparaison */}
            {isSelectedForCompare && (
              <Badge className="text-xs bg-blue-500">
                Sélectionné
              </Badge>
            )}
          </div>

          {/* Nom du CV */}
          <p className="text-sm font-medium text-slate-700 mt-1 truncate">
            📄 {entry.cvFileName}
          </p>

          {/* Aperçu de l'offre */}
          <p className="text-xs text-slate-400 mt-0.5 truncate">
            {entry.jobOfferPreview}
          </p>

          {/* Date */}
          <p className="text-xs text-slate-400 mt-1">
            🕐 {formatDate(entry.date)}
          </p>
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-1 shrink-0">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onView(entry)}
            className="text-xs h-7"
          >
            Revoir
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => onCompare(entry.id)}
            className={`text-xs h-7 ${isSelectedForCompare ? "border-blue-400 text-blue-600" : ""}`}
          >
            {isSelectedForCompare ? "✓ Comp." : "Comparer"}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onDelete(entry.id)}
            className="text-xs h-7 text-red-400 hover:text-red-600"
          >
            ✕
          </Button>
        </div>
      </div>
    </div>
  )
}

export default function HistoryPanel({
  history,
  compareIds,
  onCompare,
  onDelete,
  onView,
  onClear,
  onStartCompare,
}) {
  // Pas d'historique = rien à afficher
  if (history.length === 0) return null

  return (
    <Card className="w-full">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg text-slate-700">
            📋 Historique de session
          </CardTitle>
          <div className="flex gap-2">
            {/* Bouton comparer — actif seulement si 2 entrées sélectionnées */}
            {compareIds.length === 2 && (
              <Button
                size="sm"
                onClick={onStartCompare}
                className="text-xs"
              >
                Comparer les 2
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={onClear}
              className="text-xs text-slate-400"
            >
              Tout effacer
            </Button>
          </div>
        </div>

        {/* Aide pour la comparaison */}
        {compareIds.length === 1 && (
          <p className="text-xs text-blue-500 mt-1">
            Sélectionnez une 2e analyse pour comparer
          </p>
        )}
      </CardHeader>

      <CardContent className="space-y-2">
        {history.map(entry => (
          <HistoryEntry
            key={entry.id}
            entry={entry}
            isSelectedForCompare={compareIds.includes(entry.id)}
            onCompare={onCompare}
            onDelete={onDelete}
            onView={onView}
          />
        ))}
      </CardContent>
    </Card>
  )
}