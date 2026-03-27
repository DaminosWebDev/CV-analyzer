// frontend/app/layout.js
import "./globals.css"

export const metadata = {
  title: "CV Analyzer AI",
  description: "Analysez le match entre votre CV et une offre d'emploi",
}

export default function RootLayout({ children }) {
  return (
    <html lang="fr" style={{ background: "#0f1117" }}>
      <body style={{
        background: "#0f1117",
        color: "#e2e8f0",
        margin: 0,
        padding: 0,
        fontFamily: "system-ui, sans-serif",
        WebkitFontSmoothing: "antialiased",
      }}>
        {children}
      </body>
    </html>
  )
}