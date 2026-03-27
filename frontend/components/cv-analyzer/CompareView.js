// frontend/components/cv-analyzer/CompareView.js
// Rôle : Comparaison côte à côte de 2 analyses
// Dépendances : shadcn/ui Card Badge Button

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { formatDate } from "@/lib/storage"

function getScoreColor(score) {
  if (score >= 70) return "text-green-600"
  if (score >= 40) return "text-orange-500"
  return "text-red-500"
}

// Colonne pour une analyse dans la comparaison
function CompareColumn({ entry, isWinner }) {
  return (
    <div className={`
      flex-1 p-4 rounded-lg border-2 space-y-4
      ${isWinner ? "border-green-400 bg-green-50" : "border-slate-200 bg-white"}
    `}>
      {/* En-tête */}
      <div className="text-center space-y-1">
        {isWinner && (
          <Badge className="bg-green-500 text-white mb-1">
            🏆 Meilleur score
          </Badge>
        )}
        <div className={`text-4xl font-bold ${getScoreColor(entry.score)}`}>
          {entry.score}/100
        </div>
        <Badge variant="outline">{entry.niveau}</Badge>
        <p className="text-xs text-slate-500 truncate">
          📄 {entry.cvFileName}
        </p>
        <p className="text-xs text-slate-400">
          {formatDate(entry.date)}
        </p>
      </div>

      {/* Points forts */}
      {entry.results.points_forts?.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-green-700 mb-1">
            ✅ Points forts
          </p>
          <ul className="space-y-1">
            {entry.results.points_forts.map((p, i) => (
              <li key={i} className="text-xs text-slate-600 flex gap-1">
                <span className="text-green-500 shrink-0">•</span>{p}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Points faibles */}
      {entry.results.points_faibles?.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-red-700 mb-1">
            ⚠️ À améliorer
          </p>
          <ul className="space-y-1">
            {entry.results.points_faibles.map((p, i) => (
              <li key={i} className="text-xs text-slate-600 flex gap-1">
                <span className="text-red-400 shrink-0">•</span>{p}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Aperçu offre */}
      <div>
        <p className="text-xs font-semibold text-slate-500 mb-1">
          💼 Offre analysée
        </p>
        <p className="text-xs text-slate-400 italic">
          {entry.jobOfferPreview}
        </p>
      </div>
    </div>
  )
}

export default function CompareView({ entries, onClose }) {
  if (entries.length !== 2) return null

  const [a, b] = entries
  // Le gagnant est celui avec le score le plus élevé
  const winnerIndex = a.score >= b.score ? 0 : 1

  return (
    <Card className="w-full">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg text-slate-700">
            ⚖️ Comparaison
          </CardTitle>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            className="text-slate-400"
          >
            ✕ Fermer
          </Button>
        </div>

        {/* Différence de score */}
        <p className="text-sm text-slate-500">
          Écart : {" "}
          <span className="font-semibold text-slate-700">
            {Math.abs(a.score - b.score)} points
          </span>
        </p>
      </CardHeader>

      <CardContent>
        {/* Colonnes côte à côte */}
        <div className="flex gap-3">
          <CompareColumn entry={a} isWinner={winnerIndex === 0} />
          <CompareColumn entry={b} isWinner={winnerIndex === 1} />
        </div>
      </CardContent>
    </Card>
  )
}