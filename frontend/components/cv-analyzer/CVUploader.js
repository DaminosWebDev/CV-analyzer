// frontend/components/cv-analyzer/CVUploader.js
// Rôle : Zone d'upload du CV (drag & drop + clic)
// Dépendances : shadcn/ui Card, Badge — hook useRef, useState

import { useRef } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export default function CVUploader({ cvFile, cvText, onFileSelect, error }) {
  // useRef pointe vers l'élément <input type="file"> caché
  // On s'en sert pour déclencher l'ouverture du sélecteur de fichiers
  const inputRef = useRef(null)

  const handleClick = () => {
    inputRef.current?.click()
  }

  const handleChange = (e) => {
    const file = e.target.files?.[0]
    if (file) onFileSelect(file)
  }

  // Gestion du drag & drop
  const handleDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file) onFileSelect(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault() // Nécessaire pour autoriser le drop
  }

  // Détermine l'apparence selon l'état
  const isUploaded = !!cvText
  const hasError = !!error

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-slate-700">
        Votre CV (PDF)
      </label>

      {/* Zone de drop — input file caché derrière */}
      <Card
        onClick={handleClick}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className={`
          cursor-pointer transition-colors border-2 border-dashed
          ${isUploaded
            ? "border-green-400 bg-green-50"
            : "border-slate-200 hover:border-slate-400 bg-white"
          }
          ${hasError ? "border-red-400 bg-red-50" : ""}
        `}
      >
        <CardContent className="flex flex-col items-center justify-center py-8 gap-2">

          {/* Icône selon l'état */}
          <span className="text-3xl">
            {isUploaded ? "✅" : "📄"}
          </span>

          {/* Texte selon l'état */}
          {isUploaded ? (
            <div className="text-center">
              <p className="font-medium text-green-700">{cvFile?.name}</p>
              <p className="text-xs text-green-600 mt-1">
                {cvText.length} caractères extraits
              </p>
            </div>
          ) : (
            <div className="text-center">
              <p className="text-slate-600">
                Glissez votre CV ici ou{" "}
                <span className="text-blue-600 underline">cliquez pour parcourir</span>
              </p>
              <p className="text-xs text-slate-400 mt-1">PDF uniquement — 5 Mo max</p>
            </div>
          )}

        </CardContent>
      </Card>

      {/* Input file caché — le vrai mécanisme d'upload */}
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleChange}
        className="hidden"
      />

      {/* Badge si upload réussi */}
      {isUploaded && (
        <Badge variant="outline" className="text-green-600 border-green-400">
          CV chargé avec succès
        </Badge>
      )}
    </div>
  )
}