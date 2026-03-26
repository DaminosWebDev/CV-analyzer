// frontend/components/cv-analyzer/ScoreCard.js
// Rôle : Affiche le score de compatibilité + niveau + points forts/faibles
// Dépendances : shadcn/ui Card, Badge, Progress

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"

// Détermine la couleur selon le score
// Analogie : feux tricolores — rouge/orange/vert
function getScoreColor(score) {
  if (score >= 70) return "text-green-600"
  if (score >= 40) return "text-orange-500"
  return "text-red-500"
}

function getProgressColor(score) {
  if (score >= 70) return "bg-green-500"
  if (score >= 40) return "bg-orange-500"
  return "bg-red-500"
}

function getNiveauColor(niveau) {
  const colors = {
    "Expert":        "bg-green-100 text-green-700 border-green-300",
    "Confirmé":      "bg-blue-100 text-blue-700 border-blue-300",
    "Intermédiaire": "bg-orange-100 text-orange-700 border-orange-300",
    "Débutant":      "bg-red-100 text-red-700 border-red-300",
  }
  // Retourne une couleur par défaut si le niveau n'est pas reconnu
  return colors[niveau] || "bg-slate-100 text-slate-700 border-slate-300"
}

export default function ScoreCard({ results }) {
  // Si pas de résultats, on n'affiche rien
  if (!results) return null

  const { score, niveau, points_forts, points_faibles, justification } = results

  return (
    <Card className="w-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg text-slate-700">
          Score de compatibilité
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-6">

        {/* Score principal + barre de progression */}
        <div className="space-y-2">
          <div className="flex items-end gap-2">
            <span className={`text-6xl font-bold ${getScoreColor(score)}`}>
              {score}
            </span>
            <span className="text-2xl text-slate-400 mb-2">/100</span>
            <Badge
              variant="outline"
              className={`ml-2 mb-2 ${getNiveauColor(niveau)}`}
            >
              {niveau}
            </Badge>
          </div>

          {/* Barre de progression colorée */}
          <div className="relative h-3 w-full rounded-full bg-slate-100 overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-700 ${getProgressColor(score)}`}
              style={{ width: `${score}%` }}
            />
          </div>
        </div>

        {/* Justification du score */}
        {justification && (
          <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
            <p className="text-sm text-slate-600 italic">
              💬 {justification}
            </p>
          </div>
        )}

        {/* Points forts */}
        {points_forts?.length > 0 && (
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-green-700 flex items-center gap-1">
              <span>✅</span> Points forts
            </h3>
            <ul className="space-y-1">
              {points_forts.map((point, index) => (
                <li
                  key={index}
                  className="text-sm text-slate-600 flex items-start gap-2"
                >
                  <span className="text-green-500 mt-0.5">•</span>
                  {point}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Points faibles */}
        {points_faibles?.length > 0 && (
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-red-700 flex items-center gap-1">
              <span>⚠️</span> Points à améliorer
            </h3>
            <ul className="space-y-1">
              {points_faibles.map((point, index) => (
                <li
                  key={index}
                  className="text-sm text-slate-600 flex items-start gap-2"
                >
                  <span className="text-red-400 mt-0.5">•</span>
                  {point}
                </li>
              ))}
            </ul>
          </div>
        )}

      </CardContent>
    </Card>
  )
}