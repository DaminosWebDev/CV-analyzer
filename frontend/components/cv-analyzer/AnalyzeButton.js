// frontend/components/cv-analyzer/AnalyzeButton.js

export default function AnalyzeButton({ onAnalyze, isLoading, isDisabled }) {
  return (
    <button
      onClick={onAnalyze}
      disabled={isDisabled || isLoading}
      style={{
        width: "100%",
        background: isDisabled || isLoading ? "var(--bg-surface-hover)" : "var(--accent)",
        color: isDisabled || isLoading ? "var(--text-muted)" : "#fff",
        border: `0.5px solid ${isDisabled || isLoading ? "var(--border)" : "var(--accent)"}`,
        borderRadius: "8px",
        padding: "11px",
        fontSize: "14px",
        fontWeight: 500,
        cursor: isDisabled || isLoading ? "not-allowed" : "pointer",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "8px",
        transition: "all 0.2s",
      }}
    >
      {isLoading ? (
        <>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2"
            style={{ animation: "spin 1s linear infinite" }}>
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
          Analyse en cours...
        </>
      ) : (
        <>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
          </svg>
          Analyser mon CV
        </>
      )}
    </button>
  )
}