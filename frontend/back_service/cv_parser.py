import io
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_bytes):
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text)


def extract_cv_text(uploaded_file):
    """Extrait le texte d'un fichier CV uploadé via st.file_uploader (PDF ou DOCX).
    Lève ValueError si le format n'est pas supporté ou si aucun texte n'a pu être extrait."""
    file_bytes = uploaded_file.getvalue()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        text = extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Format de fichier non supporté (PDF ou DOCX uniquement).")

    text = text.strip()
    if not text:
        raise ValueError("Impossible d'extraire du texte de ce fichier (PDF scanné/image non supporté).")
    return text
