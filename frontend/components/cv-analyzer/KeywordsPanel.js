// frontend/components/cv-analyzer/KeywordsPanel.js

function KeywordBadge({ keyword, present }) {
  return (
    <span style={{
      fontSize: "11px",
      padding: "3px 9px",
      borderRadius: "20px",
      background: present ? "var(--success-bg)" : "var(--danger-bg)",
      border: `0.5px solid ${present ? "var(--success-border)" : "var(--danger-border)"}`,
      color: present ? "var(--success)" : "var(--danger)",
    }}>
      {present ? "✓ " : "✗ "}{keyword}
    </span>
  )
}

function KeywordGroup({ title, keywords, present }) {
  if (!keywords?.length) return null
  return (
    <div style={{ marginBottom: "12px" }}>
      <div style={{
        fontSize: "10px", color: "var(--text-muted)",
        textTransform: "uppercase", letterSpacing: "0.06em",
        marginBottom: "6px",
      }}>
        {title}
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
        {keywords.map((kw, i) => (
          <KeywordBadge key={i} keyword={kw} present={present} />
        ))}
      </div>
    </div>
  )
}

export default function KeywordsPanel({ keywords }) {
  if (!keywords) return null
  const { techniques, soft_skills } = keywords

  return (
    <div style={{
      background: "var(--bg-surface)",
      border: "0.5px solid var(--border)",
      borderRadius: "10px", padding: "18px",
    }}>
      <div style={{
        fontSize: "11px", color: "var(--accent)",
        fontWeight: 500, letterSpacing: "0.08em",
        textTransform: "uppercase", marginBottom: "14px",
      }}>
        Analyse des compétences
      </div>

      <div style={{
        fontSize: "12px", color: "var(--text-secondary)",
        fontWeight: 500, marginBottom: "10px",
      }}>
        Compétences techniques
      </div>
      <KeywordGroup title="Présentes" keywords={techniques?.presentes} present={true} />
      <KeywordGroup title="Manquantes" keywords={techniques?.manquantes} present={false} />

      <div style={{
        borderTop: "0.5px solid var(--border)",
        marginTop: "8px", marginBottom: "12px",
      }} />

      <div style={{
        fontSize: "12px", color: "var(--text-secondary)",
        fontWeight: 500, marginBottom: "10px",
      }}>
        Soft skills
      </div>
      <KeywordGroup title="Présentes" keywords={soft_skills?.presentes} present={true} />
      <KeywordGroup title="Manquantes" keywords={soft_skills?.manquantes} present={false} />
    </div>
  )
}