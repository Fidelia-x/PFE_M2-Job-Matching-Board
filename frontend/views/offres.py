import streamlit as st
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header
from views.gating import require_matching
from views.offer_card import render_offer_card

_PAGE_SIZE = 20


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

    display_count = st.session_state.get("offres_display_count", _PAGE_SIZE)

    for offre in offres[:display_count]:
        render_offer_card(offre)

    if display_count < len(offres):
        st.markdown(f'<p class="sg-offer-meta">{display_count} sur {len(offres)} offres affichées</p>', unsafe_allow_html=True)
        if st.button("Voir plus d'offres", key="load_more_offres"):
            st.session_state.offres_display_count = display_count + _PAGE_SIZE
            st.rerun()
