// frontend/components/cv-analyzer/KeywordsPanel.js
// Rôle : Affiche les mots-clés techniques et soft skills présents/manquants
// Dépendances : shadcn/ui Card, Badge

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

// Sous-composant pour une liste de mots-clés avec badges colorés
function KeywordGroup({ title, keywords, variant }) {
  if (!keywords?.length) return null

  return (
    <div className="space-y-2">
      <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
        {title}
      </h4>
      <div className="flex flex-wrap gap-2">
        {keywords.map((keyword, index) => (
          <Badge
            key={index}
            variant="outline"
            className={
              variant === "present"
                ? "bg-green-50 text-green-700 border-green-300"
                : "bg-red-50 text-red-700 border-red-300"
            }
          >
            {variant === "present" ? "✓ " : "✗ "}
            {keyword}
          </Badge>
        ))}
      </div>
    </div>
  )
}

export default function KeywordsPanel({ keywords }) {
  if (!keywords) return null

  const { techniques, soft_skills } = keywords

  return (
    <Card className="w-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg text-slate-700">
          Analyse des compétences
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-6">

        {/* Compétences techniques */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-slate-700 flex items-center gap-2">
            <span>⚙️</span> Compétences techniques
          </h3>

          <KeywordGroup
            title="Présentes dans votre CV"
            keywords={techniques?.presentes}
            variant="present"
          />
          <KeywordGroup
            title="Manquantes — à ajouter"
            keywords={techniques?.manquantes}
            variant="missing"
          />
        </div>

        {/* Séparateur visuel */}
        <div className="border-t border-slate-100" />

        {/* Soft skills */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-slate-700 flex items-center gap-2">
            <span>🤝</span> Soft skills
          </h3>

          <KeywordGroup
            title="Présentes dans votre CV"
            keywords={soft_skills?.presentes}
            variant="present"
          />
          <KeywordGroup
            title="Manquantes — à ajouter"
            keywords={soft_skills?.manquantes}
            variant="missing"
          />
        </div>

      </CardContent>
    </Card>
  )
}