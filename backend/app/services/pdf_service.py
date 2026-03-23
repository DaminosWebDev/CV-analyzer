# backend/app/services/pdf_service.py
# Rôle       : Extraction du texte brut depuis un fichier PDF
# Dépendances: pymupdf (fitz)

import fitz  # PyMuPDF s'importe sous le nom "fitz"
import io
from typing import Optional


# Taille maximale acceptée : 10 Mo
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def extract_text_from_pdf(file_bytes: bytes) -> tuple[str, int]:
    """
    Extrait le texte brut d'un fichier PDF fourni en bytes.

    Args:
        file_bytes: contenu binaire du fichier PDF

    Returns:
        tuple (texte_extrait, nombre_de_pages)

    Raises:
        ValueError: si le fichier est invalide, trop lourd, ou sans texte
    """

    # ── Étape 1 : Vérification de la taille ──────────────────────────────────
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"Fichier trop volumineux : {len(file_bytes) / 1024 / 1024:.1f} Mo "
            f"(maximum : {MAX_FILE_SIZE_MB} Mo)"
        )

    # ── Étape 2 : Ouverture du PDF depuis la mémoire ─────────────────────────
    try:
        # On ouvre le PDF depuis les bytes en mémoire (pas de fichier temporaire)
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Impossible d'ouvrir le fichier PDF : {str(e)}")

    # ── Étape 3 : Extraction du texte page par page ───────────────────────────
    try:
        page_count = len(pdf_document)
        extracted_pages = []

        for page_number in range(page_count):
            page = pdf_document[page_number]
            # get_text() retourne le texte brut de la page
            page_text = page.get_text()
            if page_text.strip():  # ignore les pages vides
                extracted_pages.append(page_text)

        # Fermeture propre du document
        pdf_document.close()

        # ── Étape 4 : Assemblage et nettoyage ────────────────────────────────
        full_text = "\n\n".join(extracted_pages)
        full_text = clean_extracted_text(full_text)

        # ── Étape 5 : Validation du résultat ─────────────────────────────────
        if not full_text or len(full_text.strip()) < 50:
            raise ValueError(
                "Aucun texte extractible dans ce PDF. "
                "S'il s'agit d'un PDF scanné (image), "
                "veuillez copier-coller le texte directement."
            )

        return full_text, page_count

    except ValueError:
        raise  # on re-lève les ValueError qu'on a créées
    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction du texte : {str(e)}")


def clean_extracted_text(text: str) -> str:
    """
    Nettoie le texte extrait du PDF.
    Supprime les espaces excessifs et les lignes vides multiples.

    Args:
        text: texte brut extrait

    Returns:
        texte nettoyé
    """
    if not text:
        return ""

    # Supprime les espaces en début/fin de chaque ligne
    lines = [line.strip() for line in text.splitlines()]

    # Supprime les blocs de lignes vides consécutives (garde maximum 2 sauts)
    cleaned_lines = []
    empty_count = 0

    for line in lines:
        if line == "":
            empty_count += 1
            if empty_count <= 2:
                cleaned_lines.append(line)
        else:
            empty_count = 0
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def get_pdf_info(file_bytes: bytes) -> dict:
    """
    Retourne des informations basiques sur le PDF sans extraire tout le texte.
    Utile pour la validation rapide.

    Args:
        file_bytes: contenu binaire du fichier PDF

    Returns:
        dict avec page_count, file_size_kb, is_readable
    """
    try:
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        page_count = len(pdf_document)

        # Teste si la première page a du texte
        first_page_text = pdf_document[0].get_text() if page_count > 0 else ""
        is_readable = len(first_page_text.strip()) > 10

        pdf_document.close()

        return {
            "page_count": page_count,
            "file_size_kb": round(len(file_bytes) / 1024, 1),
            "is_readable": is_readable
        }
    except Exception:
        return {
            "page_count": 0,
            "file_size_kb": 0,
            "is_readable": False
        }