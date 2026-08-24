import streamlit as st


def format_salaire(mn, mx):
    def valid(v):
        return v is not None and v > 0

    mn = mn if valid(mn) else None
    mx = mx if valid(mx) else None

    def fmt(v):
        return f"{v / 1000:.0f}k€" if v >= 1000 else f"{v:.0f}€"

    if mn is not None and mx is not None:
        return f"{fmt(mn)} – {fmt(mx)}"
    if mn is not None or mx is not None:
        return fmt(mn if mn is not None else mx)
    return "Salaire non précisé"


def render_skill_pills(matched_skills, missing_skills):
    if not matched_skills and not missing_skills:
        return ""

    pills = "".join(f'<span class="sg-pill sg-pill-success">{s}</span>' for s in (matched_skills or []))
    pills += "".join(f'<span class="sg-pill sg-pill-danger">{s}</span>' for s in (missing_skills or []))
    return f'<div class="sg-offer-skills">{pills}</div>'


def render_offer_card(offre):
    """Affiche une carte d'offre (rendu identique à la version d'origine ;
    les compétences s'ajoutent en plus, en dessous, seulement quand il y en a).

    Utilise st.html() plutôt que st.markdown(..., unsafe_allow_html=True) :
    ce dernier fait passer le HTML par le parseur Markdown/CommonMark de
    Streamlit, qui applique des règles de détection de bloc HTML (indentation,
    lignes vides, tags "inline" comme <a> non reconnus comme démarrant un
    bloc...) et peut fragmenter/casser une structure HTML pourtant valide.
    st.html() insère le HTML tel quel (juste sanitizé par DOMPurify), sans
    passer par ce parseur.
    """
    url = offre.get("source_url")
    tag = "a" if url else "div"
    attrs = f' href="{url}" target="_blank" rel="noopener noreferrer"' if url else ""
    skills_html = render_skill_pills(offre.get("matched_skills"), offre.get("missing_skills"))

    st.html(f"""
    <{tag} class="sg-offer-card"{attrs}>
        <div>
            <p class="sg-offer-title">{offre['titre']}</p>
            <p class="sg-offer-meta">{offre['company']} · {offre.get('localisation') or 'Lieu non précisé'} · {offre.get('contract') or 'Contrat non précisé'} · {format_salaire(offre.get('salaire_min'), offre.get('salaire_max'))}</p>
        </div>
        <div>
            <div class="sg-offer-score">{round(offre['score'] * 100)}%</div>
            <div class="sg-offer-score-label">Correspondance</div>
        </div>
        {skills_html}
    </{tag}>
    """)
