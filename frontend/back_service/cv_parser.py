import io
import pdfplumber
from docx import Document

from back_service.mistral_client import get_client


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


def extract_target_role(cv_text):
    """Détecte le poste visé tel qu'il est écrit sur le CV (titre en tête de
    CV, objectif professionnel, intitulé du poste le plus récent...).

    Extraction factuelle, pas une supposition : le prompt demande
    explicitement de ne rien inventer si ce n'est indiqué nulle part dans le
    texte, plutôt que de deviner un intitulé plausible.

    Tronque à 4000 caractères : l'intitulé/l'objectif visé se trouve presque
    toujours dans l'en-tête du CV, pas besoin d'envoyer le document entier.

    Retourne l'intitulé (str) ou None si absent du texte ou si Mistral n'est
    pas joignable."""
    client = get_client()
    if client is None:
        return None

    prompt = f"""Voici le texte d'un CV :

{cv_text[:4000]}

Quel est l'intitulé du poste visé par ce candidat, tel qu'il apparaît explicitement dans le CV (titre en tête de CV, objectif professionnel, intitulé du poste le plus récent...) ?

Réponds uniquement par l'intitulé du poste (2 à 4 mots), sans phrase autour. Si aucun poste visé n'est indiqué explicitement dans le texte, réponds exactement : Non précisé"""

    try:
        response = client.chat.complete(model="mistral-small-latest", messages=[{"role": "user", "content": prompt}])
        role = response.choices[0].message.content.strip()
    except Exception:
        return None

    return None if role.lower().startswith("non précisé") else role
