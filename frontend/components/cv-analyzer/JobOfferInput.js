// frontend/components/cv-analyzer/JobOfferInput.js

export default function JobOfferInput({ value, onChange }) {
  const charCount = value.length
  const isValid = charCount >= 50

  return (
    <div>
      <div style={{
        display: "flex", justifyContent: "space-between",
        alignItems: "center", marginBottom: "8px",
      }}>
        <div style={{
          fontSize: "11px", color: "var(--accent)",
          fontWeight: 500, letterSpacing: "0.08em",
          textTransform: "uppercase",
        }}>
          Offre d'emploi
        </div>
        <span style={{
          fontSize: "11px",
          color: isValid ? "var(--success)" : "var(--text-muted)",
        }}>
          {charCount.toLocaleString()} car.{isValid ? " ✓" : " (min. 50)"}
        </span>
      </div>

      <textarea
        placeholder="Collez ici le texte complet de l'offre d'emploi..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{
          width: "100%",
          minHeight: "140px",
          background: "var(--bg-surface)",
          border: `0.5px solid ${isValid ? "var(--success-border)" : "var(--border)"}`,
          borderRadius: "10px",
          padding: "12px 14px",
          color: "var(--text-primary)",
          fontSize: "12px",
          fontFamily: "var(--font-mono, monospace)",
          lineHeight: "1.6",
          resize: "vertical",
          outline: "none",
          transition: "border-color 0.2s",
        }}
        onFocus={e => {
          if (!isValid) e.target.style.borderColor = "var(--accent)"
        }}
        onBlur={e => {
          e.target.style.borderColor = isValid
            ? "var(--success-border)" : "var(--border)"
        }}
      />
    </div>
  )
}