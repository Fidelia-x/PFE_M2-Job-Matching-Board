import streamlit as st
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header
from views.gating import require_matching


def _format_salaire(mn, mx):
    def valid(v):
        return v is not None and v >= 0

    mn = mn if valid(mn) else None
    mx = mx if valid(mx) else None

    def fmt(v):
        return f"{v / 1000:.0f}k€" if v >= 1000 else f"{v:.0f}€"

    if mn is not None and mx is not None:
        return f"{fmt(mn)} – {fmt(mx)}"
    if mn is not None or mx is not None:
        return fmt(mn if mn is not None else mx)
    return "Salaire non précisé"


def render_offres():
    inject_dashboard_style()
    render_sidebar(active_page="offres")
    render_header(subtitle="Voici les offres d'emploi correspondant à votre profil", title="Offres d'emploi")

    if not require_matching():
        return

    offres = st.session_state.get("matched_offers", [])
    if not offres:
        st.info("Aucune offre correspondante trouvée pour le moment.")
        return

    for offre in offres:
        url = offre.get("source_url")
        tag_open = f'<a class="sg-offer-card" href="{url}" target="_blank" rel="noopener noreferrer">' if url else '<div class="sg-offer-card">'
        tag_close = "</a>" if url else "</div>"
        st.markdown(f"""
        {tag_open}
            <div>
                <p class="sg-offer-title">{offre['titre']}</p>
                <p class="sg-offer-meta">{offre['company']} · {offre.get('localisation') or 'Lieu non précisé'} · {offre.get('contract') or 'Contrat non précisé'} · {_format_salaire(offre.get('salaire_min'), offre.get('salaire_max'))}</p>
            </div>
            <div>
                <div class="sg-offer-score">{round(offre['score'] * 100)}%</div>
                <div class="sg-offer-score-label">Correspondance</div>
            </div>
        {tag_close}
        """, unsafe_allow_html=True)
