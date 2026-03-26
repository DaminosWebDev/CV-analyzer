// frontend/components/layout/Header.js
// Rôle : Barre de navigation fixe en haut de la page
// Dépendances : aucune

export default function Header() {
  return (
    <header className="border-b bg-white sticky top-0 z-10">
      <div className="container mx-auto px-4 h-14 flex items-center justify-between">

        {/* Logo + nom de l'app */}
        <div className="flex items-center gap-2">
          <span className="text-xl">🎯</span>
          <span className="font-bold text-slate-800">CV Analyzer AI</span>
        </div>

        {/* Badge RGPD — argument portfolio important */}
        <div className="flex items-center gap-1 text-xs text-slate-500">
          <span>🔒</span>
          <span>Aucune donnée stockée — RGPD friendly</span>
        </div>

      </div>
    </header>
  )
}