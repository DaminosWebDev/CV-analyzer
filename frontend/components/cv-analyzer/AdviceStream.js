// frontend/components/cv-analyzer/AdviceStream.js

import { useEffect } from "react"

export default function AdviceStream({ advice, isStreaming, onStreamComplete }) {
  useEffect(() => {
    if (!isStreaming && advice) {
      onStreamComplete?.()
    }
  }, [isStreaming])

  if (!advice && !isStreaming) return null

  return (
    <div style={{
      background: "var(--bg-surface)",
      border: "0.5px solid var(--border)",
      borderRadius: "10px", padding: "18px",
    }}>
      <div style={{
        display: "flex", alignItems: "center",
        gap: "8px", marginBottom: "12px",
      }}>
        {isStreaming && (
          <div style={{
            width: "6px", height: "6px",
            borderRadius: "50%", background: "var(--accent)",
            animation: "pulse 1.5s infinite",
          }} />
        )}
        <div style={{
          fontSize: "11px", color: "var(--accent)",
          fontWeight: 500, letterSpacing: "0.08em",
          textTransform: "uppercase",
        }}>
          Conseils personnalisés
          {isStreaming && (
            <span style={{ color: "var(--text-muted)", fontWeight: 400, textTransform: "none", letterSpacing: 0 }}>
              {" "}· génération en cours
            </span>
          )}
        </div>
      </div>

      <p style={{
        color: "var(--text-secondary)",
        fontSize: "13px", lineHeight: 1.75,
        whiteSpace: "pre-wrap",
      }}>
        {advice}
        {isStreaming && (
          <span style={{
            display: "inline-block",
            width: "2px", height: "14px",
            background: "var(--accent)",
            marginLeft: "2px",
            verticalAlign: "middle",
            animation: "blink 1s infinite",
          }} />
        )}
      </p>

      <style>{`
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
      `}</style>
    </div>
  )
}