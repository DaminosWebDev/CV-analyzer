// frontend/components/cv-analyzer/JobOfferInput.js
// Rôle : Textarea pour coller l'offre d'emploi
// Dépendances : shadcn/ui Textarea, Badge

import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"

export default function JobOfferInput({ value, onChange }) {
  const charCount = value.length
  // Offre considérée valide à partir de 50 caractères
  const isValid = charCount >= 50

  return (
    <div className="space-y-2">

      {/* Label + compteur de caractères */}
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium text-slate-700">
          Offre d'emploi
        </label>
        <span className={`text-xs ${isValid ? "text-green-600" : "text-slate-400"}`}>
          {charCount} caractères {isValid ? "✓" : "(min. 50)"}
        </span>
      </div>

      <Textarea
        placeholder="Collez ici le texte complet de l'offre d'emploi..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="min-h-48 resize-y font-mono text-sm"
      />

      {/* Indication visuelle si l'offre est prête */}
      {isValid && (
        <Badge variant="outline" className="text-green-600 border-green-400">
          Offre prête pour l'analyse
        </Badge>
      )}

    </div>
  )
}