// frontend/components/cv-analyzer/ScoreCard.js

function getScoreColor(score) {
  if (score >= 70) return "var(--success)"
  if (score >= 40) return "var(--warning)"
  return "var(--danger)"
}

function getNiveauStyle(niveau) {
  const styles = {
    "Expert":        { bg: "var(--success-bg)", border: "var(--success-border)", color: "var(--success)" },
    "Confirmé":      { bg: "#0d1a2e", border: "#1e3a5f", color: "#60a5fa" },
    "Intermédiaire": { bg: "var(--warning-bg)", border: "var(--warning-border)", color: "var(--warning)" },
    "Débutant":      { bg: "var(--danger-bg)", border: "var(--danger-border)", color: "var(--danger)" },
  }
  return styles[niveau] || { bg: "var(--bg-surface-hover)", border: "var(--border)", color: "var(--text-secondary)" }
}

export default function ScoreCard({ results }) {
  if (!results) return null
  const { score, niveau, points_forts, points_faibles, justification } = results
  const niveauStyle = getNiveauStyle(niveau)

  return (
    <div style={{
      background: "var(--bg-surface)",
      border: "0.5px solid var(--border)",
      borderRadius: "10px",
      padding: "18px",
    }}>
      <div style={{
        fontSize: "11px", color: "var(--accent)",
        fontWeight: 500, letterSpacing: "0.08em",
        textTransform: "uppercase", marginBottom: "14px",
      }}>
        Score de compatibilité
      </div>

      {/* Score + niveau */}
      <div style={{ display: "flex", alignItems: "flex-end", gap: "8px", marginBottom: "10px" }}>
        <span style={{
          fontSize: "52px", fontWeight: 700,
          color: getScoreColor(score), lineHeight: 1,
        }}>
          {score}
        </span>
        <span style={{ color: "var(--text-muted)", fontSize: "20px", marginBottom: "6px" }}>
          /100
        </span>
        <div style={{
          ...niveauStyle,
          fontSize: "11px", padding: "3px 10px",
          borderRadius: "20px", border: `0.5px solid ${niveauStyle.border}`,
          marginBottom: "6px",
        }}>
          {niveau}
        </div>
      </div>

      {/* Barre de progression */}
      <div style={{
        background: "var(--bg-surface-hover)",
        borderRadius: "4px", height: "6px",
        overflow: "hidden", marginBottom: "16px",
      }}>
        <div style={{
          width: `${score}%`, height: "100%",
          background: getScoreColor(score),
          borderRadius: "4px",
          transition: "width 0.8s ease",
        }} />
      </div>

      {/* Justification */}
      {justification && (
        <div style={{
          background: "var(--bg-surface-hover)",
          border: "0.5px solid var(--border)",
          borderRadius: "8px", padding: "10px 12px",
          marginBottom: "16px",
        }}>
          <p style={{ color: "var(--text-secondary)", fontSize: "12px", lineHeight: 1.6 }}>
            {justification}
          </p>
        </div>
      )}

      {/* Points forts */}
      {points_forts?.length > 0 && (
        <div style={{ marginBottom: "12px" }}>
          <div style={{
            fontSize: "11px", color: "var(--success)",
            fontWeight: 500, marginBottom: "6px",
          }}>
            Points forts
          </div>
          {points_forts.map((p, i) => (
            <div key={i} style={{
              display: "flex", gap: "8px",
              fontSize: "12px", color: "var(--text-secondary)",
              lineHeight: 1.6, marginBottom: "2px",
            }}>
              <span style={{ color: "var(--success)", flexShrink: 0 }}>›</span>
              {p}
            </div>
          ))}
        </div>
      )}

      {/* Points faibles */}
      {points_faibles?.length > 0 && (
        <div>
          <div style={{
            fontSize: "11px", color: "var(--danger)",
            fontWeight: 500, marginBottom: "6px",
          }}>
            À améliorer
          </div>
          {points_faibles.map((p, i) => (
            <div key={i} style={{
              display: "flex", gap: "8px",
              fontSize: "12px", color: "var(--text-secondary)",
              lineHeight: 1.6, marginBottom: "2px",
            }}>
              <span style={{ color: "var(--danger)", flexShrink: 0 }}>›</span>
              {p}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}