// frontend/app/page.js
"use client"

import { useState } from "react"
import Header from "@/components/layout/Header"
import CVUploader from "@/components/cv-analyzer/CVUploader"
import JobOfferInput from "@/components/cv-analyzer/JobOfferInput"
import AnalyzeButton from "@/components/cv-analyzer/AnalyzeButton"
import ScoreCard from "@/components/cv-analyzer/ScoreCard"
import KeywordsPanel from "@/components/cv-analyzer/KeywordsPanel"
import AdviceStream from "@/components/cv-analyzer/AdviceStream"
import HistoryPanel from "@/components/cv-analyzer/HistoryPanel"
import CompareView from "@/components/cv-analyzer/CompareView"
import { useAnalyzer } from "@/hooks/useAnalyzer"
import { useHistory } from "@/hooks/useHistory"

export default function Home() {
  const {
    cvFile, cvText, jobOffer, error,
    results, advice, isStreaming, step,
    handleFileSelect, handleJobOfferChange,
    handleAnalyze, handleReset,
  } = useAnalyzer()

  const {
    history, addToHistory, removeFromHistory,
    resetHistory, compareIds, toggleCompare,
    clearCompare, compareEntries,
  } = useHistory()

  const [showCompare, setShowCompare] = useState(false)

  const isLoading = step === "loading"
  const isReady = !!cvText && jobOffer.length >= 50
  const hasResults = !!results

  const handleSaveComplete = () => {
    if (results && advice && !isStreaming) {
      addToHistory(cvFile?.name || "CV sans nom", jobOffer, results, advice)
    }
  }

  return (
    <div style={{ minHeight: "100vh", background: "var(--bg-primary)" }}>
      <Header />

      <main style={{
        maxWidth: "1200px",
        margin: "0 auto",
        padding: "32px 24px",
        // Grille 2 colonnes FIXE — toujours présente
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "24px",
        alignItems: "start",
      }}>

        {/* ══════════════════════════════
            COLONNE GAUCHE — Formulaire
        ══════════════════════════════ */}
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>

          {/* Titre */}
          <div>
            <h1 style={{
              fontSize: "22px", fontWeight: 600,
              color: "var(--text-primary)", marginBottom: "4px",
            }}>
              Analysez votre CV
            </h1>
            <p style={{ color: "var(--text-muted)", fontSize: "13px" }}>
              Uploadez votre CV et collez une offre d'emploi.
            </p>
          </div>

          <CVUploader
            cvFile={cvFile}
            cvText={cvText}
            onFileSelect={handleFileSelect}
          />

          <JobOfferInput value={jobOffer} onChange={handleJobOfferChange} />

          {error && (
            <div style={{
              background: "var(--danger-bg)",
              border: "0.5px solid var(--danger-border)",
              borderRadius: "8px", padding: "10px 12px",
              fontSize: "12px", color: "var(--danger)",
            }}>
              {error}
            </div>
          )}

          <AnalyzeButton
            onAnalyze={handleAnalyze}
            isLoading={isLoading}
            isDisabled={!isReady}
          />

          {hasResults && (
            <button
              onClick={handleReset}
              style={{
                background: "transparent",
                border: "0.5px solid var(--border)",
                borderRadius: "8px", padding: "8px",
                fontSize: "12px", color: "var(--text-muted)",
                cursor: "pointer", width: "100%",
              }}
            >
              ← Nouvelle analyse (CV conservé)
            </button>
          )}

          <HistoryPanel
            history={history}
            compareIds={compareIds}
            onCompare={toggleCompare}
            onDelete={removeFromHistory}
            onView={() => {}}
            onClear={resetHistory}
            onStartCompare={() => setShowCompare(true)}
          />

          {showCompare && compareEntries.length === 2 && (
            <CompareView
              entries={compareEntries}
              onClose={() => { setShowCompare(false); clearCompare() }}
            />
          )}
        </div>

        {/* ══════════════════════════════
            COLONNE DROITE — Résultats
        ══════════════════════════════ */}
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>

          {/* État vide — avant la première analyse */}
          {!hasResults && !isLoading && (
            <div style={{
              background: "var(--bg-surface)",
              border: "1.5px dashed var(--border)",
              borderRadius: "10px",
              padding: "48px 24px",
              textAlign: "center",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "12px",
            }}>
              {/* Icône */}
              <div style={{
                width: "48px", height: "48px",
                background: "var(--bg-surface-hover)",
                borderRadius: "12px",
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
                  stroke="var(--accent)" strokeWidth="1.5">
                  <circle cx="11" cy="11" r="8"/>
                  <path d="m21 21-4.35-4.35"/>
                </svg>
              </div>
              <div>
                <p style={{
                  color: "var(--text-secondary)",
                  fontSize: "14px", fontWeight: 500,
                  marginBottom: "4px",
                }}>
                  Résultats de l'analyse
                </p>
                <p style={{ color: "var(--text-muted)", fontSize: "12px" }}>
                  Uploadez votre CV et collez une offre,<br/>
                  puis cliquez sur "Analyser mon CV".
                </p>
              </div>
            </div>
          )}

          {/* État chargement */}
          {isLoading && (
            <div style={{
              background: "var(--bg-surface)",
              border: "0.5px solid var(--border)",
              borderRadius: "10px",
              padding: "48px 24px",
              textAlign: "center",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "16px",
            }}>
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none"
                stroke="var(--accent)" strokeWidth="2"
                style={{ animation: "spin 1s linear infinite" }}>
                <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
              </svg>
              <div>
                <p style={{
                  color: "var(--text-secondary)",
                  fontSize: "14px", fontWeight: 500,
                  marginBottom: "4px",
                }}>
                  Analyse en cours...
                </p>
                <p style={{ color: "var(--text-muted)", fontSize: "12px" }}>
                  Le LLM analyse votre CV et l'offre d'emploi.
                </p>
              </div>
            </div>
          )}

          {/* Résultats */}
          {hasResults && (
            <>
              <ScoreCard results={results} />
              <KeywordsPanel keywords={results?.keywords} />
              <AdviceStream
                advice={advice}
                isStreaming={isStreaming}
                onStreamComplete={handleSaveComplete}
              />
            </>
          )}

        </div>
      </main>

      <style>{`
        @keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
        @media (max-width: 768px) {
          main {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </div>
  )
}