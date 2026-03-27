// frontend/components/layout/Header.js

export default function Header() {
  return (
    <header style={{
      background: "var(--bg-surface)",
      borderBottom: "0.5px solid var(--border)",
      padding: "0 24px",
      height: "52px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      position: "sticky",
      top: 0,
      zIndex: 10,
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <div style={{
          width: "8px", height: "8px",
          borderRadius: "50%",
          background: "var(--accent)",
        }} />
        <span style={{
          color: "var(--text-primary)",
          fontSize: "15px",
          fontWeight: 500,
        }}>
          CV Analyzer AI
        </span>
      </div>
      <div style={{
        display: "flex", alignItems: "center", gap: "6px",
        fontSize: "11px", color: "var(--text-muted)",
      }}>
        <div style={{
          width: "6px", height: "6px",
          borderRadius: "50%", background: "#22c55e",
        }} />
        Aucune donnée stockée — RGPD friendly
      </div>
    </header>
  )
}