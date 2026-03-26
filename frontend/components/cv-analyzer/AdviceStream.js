// frontend/components/cv-analyzer/AdviceStream.js
// Rôle : Affiche les conseils personnalisés qui arrivent token par token (SSE)
// Dépendances : shadcn/ui Card

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function AdviceStream({ advice, isStreaming }) {
  // Rien à afficher si pas encore de conseils
  if (!advice && !isStreaming) return null

  return (
    <Card className="w-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg text-slate-700 flex items-center gap-2">
          <span>💡</span>
          Conseils personnalisés
          {/* Indicateur animé pendant le streaming */}
          {isStreaming && (
            <span className="flex items-center gap-1 text-sm font-normal text-blue-500">
              <span className="animate-pulse">●</span>
              Génération en cours...
            </span>
          )}
        </CardTitle>
      </CardHeader>

      <CardContent>
        <div className="prose prose-sm max-w-none">
          {/* Le texte s'accumule token par token */}
          <p className="text-slate-600 whitespace-pre-wrap leading-relaxed">
            {advice}
            {/* Curseur clignotant pendant le streaming */}
            {isStreaming && (
              <span className="inline-block w-0.5 h-4 bg-blue-500 animate-pulse ml-0.5 align-middle" />
            )}
          </p>
        </div>
      </CardContent>
    </Card>
  )
}