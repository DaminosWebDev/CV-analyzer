// frontend/components/cv-analyzer/AnalyzeButton.js
// Rôle : Bouton de lancement de l'analyse avec états visuels
// Dépendances : shadcn/ui Button

import { Button } from "@/components/ui/button.jsx"

export default function AnalyzeButton({ onAnalyze, isLoading, isDisabled }) {
  return (
    <Button
      onClick={onAnalyze}
      disabled={isDisabled || isLoading}
      size="lg"
      className="w-full"
    >
      {isLoading ? (
        // Spinner animé pendant le chargement
        <span className="flex items-center gap-2">
          <span className="animate-spin">⏳</span>
          Analyse en cours...
        </span>
      ) : (
        <span className="flex items-center gap-2">
          <span>🚀</span>
          Analyser mon CV
        </span>
      )}
    </Button>
  )
}