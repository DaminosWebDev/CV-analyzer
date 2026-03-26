// frontend/app/page.js
// Rôle : Page principale complète — formulaire + résultats
// Dépendances : useAnalyzer + tous les composants

"use client"

import Header from "@/components/layout/Header"
import CVUploader from "@/components/cv-analyzer/CVUploader"
import JobOfferInput from "@/components/cv-analyzer/JobOfferInput"
import AnalyzeButton from "@/components/cv-analyzer/AnalyzeButton"
import ScoreCard from "@/components/cv-analyzer/ScoreCard"
import KeywordsPanel from "@/components/cv-analyzer/KeywordsPanel"
import AdviceStream from "@/components/cv-analyzer/AdviceStream"
import { useAnalyzer } from "@/hooks/useAnalyzer"

export default function Home() {
  const {
    step,
    cvFile,
    cvText,
    jobOffer,
    error,
    results,
    advice,
    isStreaming,
    handleFileSelect,
    handleJobOfferChange,
    handleAnalyze,
    handleReset,
  } = useAnalyzer()

  const isLoading = step === "loading"
  const isReady = !!cvText && jobOffer.length >= 50

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />

      <main className="container mx-auto px-4 py-8 max-w-2xl">

        {/* Titre */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-slate-800">
            Analysez votre CV
          </h1>
          <p className="text-slate-500 mt-2">
            Uploadez votre CV et collez une offre d'emploi pour obtenir
            votre score de compatibilité.
          </p>
        </div>

        {/* ── FORMULAIRE (étapes input + loading) ── */}
        {step !== "results" && (
          <div className="space-y-6">
            <CVUploader
              cvFile={cvFile}
              cvText={cvText}
              onFileSelect={handleFileSelect}
              error={error}
            />
            <JobOfferInput
              value={jobOffer}
              onChange={handleJobOfferChange}
            />
            {error && (
              <div className="p-3 rounded-md bg-red-50 border border-red-200">
                <p className="text-sm text-red-600">⚠️ {error}</p>
              </div>
            )}
            <AnalyzeButton
              onAnalyze={handleAnalyze}
              isLoading={isLoading}
              isDisabled={!isReady}
            />
          </div>
        )}

        {/* ── RÉSULTATS ── */}
        {step === "results" && (
          <div className="space-y-6">

            {/* Bouton retour */}
            <button
              onClick={handleReset}
              className="text-sm text-blue-600 hover:underline flex items-center gap-1"
            >
              ← Nouvelle analyse
            </button>

            {/* Score */}
            <ScoreCard results={results} />

            {/* Mots-clés */}
            <KeywordsPanel keywords={results?.keywords} />

            {/* Conseils streaming */}
            <AdviceStream advice={advice} isStreaming={isStreaming} />

          </div>
        )}

      </main>
    </div>
  )
}