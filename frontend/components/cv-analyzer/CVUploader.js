// frontend/components/cv-analyzer/CVUploader.js

import { useRef } from "react"

export default function CVUploader({ cvFile, cvText, onFileSelect }) {
  const inputRef = useRef(null)

  const handleDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file) onFileSelect(file)
  }

  const isUploaded = !!cvText

  return (
    <div>
      <div style={{
        fontSize: "11px", color: "var(--accent)",
        fontWeight: 500, letterSpacing: "0.08em",
        textTransform: "uppercase", marginBottom: "8px",
      }}>
        Votre CV
      </div>

      {isUploaded ? (
        // État : CV chargé
        <div
          onClick={() => inputRef.current?.click()}
          style={{
            background: "var(--success-bg)",
            border: "1.5px solid var(--success-border)",
            borderRadius: "10px", padding: "14px 16px",
            display: "flex", alignItems: "center",
            gap: "12px", cursor: "pointer",
          }}
        >
          <div style={{
            width: "30px", height: "30px", borderRadius: "50%",
            background: "var(--success-border)",
            display: "flex", alignItems: "center", justifyContent: "center",
            flexShrink: 0,
          }}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
              stroke="#4ade80" strokeWidth="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{
              color: "var(--success)", fontSize: "13px",
              fontWeight: 500, whiteSpace: "nowrap",
              overflow: "hidden", textOverflow: "ellipsis",
            }}>
              {cvFile?.name}
            </div>
            <div style={{ color: "#16a34a", fontSize: "11px", marginTop: "2px" }}>
              {cvText.length.toLocaleString()} caractères extraits
              · Cliquer pour changer
            </div>
          </div>
        </div>
      ) : (
        // État : pas encore de CV
        <div
          onClick={() => inputRef.current?.click()}
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          style={{
            background: "var(--bg-surface)",
            border: "1.5px dashed var(--border)",
            borderRadius: "10px", padding: "28px",
            textAlign: "center", cursor: "pointer",
            transition: "border-color 0.2s",
          }}
          onMouseEnter={e => e.currentTarget.style.borderColor = "var(--accent)"}
          onMouseLeave={e => e.currentTarget.style.borderColor = "var(--border)"}
        >
          <div style={{
            width: "36px", height: "36px",
            background: "var(--bg-surface-hover)",
            borderRadius: "8px", margin: "0 auto 12px",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
              stroke="var(--accent)" strokeWidth="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="12" y1="18" x2="12" y2="12"/>
              <line x1="9" y1="15" x2="15" y2="15"/>
            </svg>
          </div>
          <div style={{ color: "var(--text-secondary)", fontSize: "13px" }}>
            Glissez votre CV ici ou{" "}
            <span style={{ color: "var(--accent)" }}>cliquez pour parcourir</span>
          </div>
          <div style={{
            color: "var(--text-muted)", fontSize: "11px", marginTop: "4px",
          }}>
            PDF uniquement — 5 Mo max
          </div>
        </div>
      )}

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,application/pdf"
        onChange={(e) => {
          const file = e.target.files?.[0]
          if (file) onFileSelect(file)
        }}
        style={{ display: "none" }}
      />
    </div>
  )
}