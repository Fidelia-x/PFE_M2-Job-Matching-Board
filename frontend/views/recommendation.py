import streamlit as st
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header
from views.gating import require_matching
from views.mock_data import MOCK_TRAININGS

def render_recommendation():
    inject_dashboard_style()
    render_sidebar(active_page="recommendation")
    render_header(subtitle="Voici les recommandations de formations adaptées à votre profil pour combler vos écarts", title="Recommandations de formations")

    if not require_matching():
        return

    for formation in MOCK_TRAININGS:
        st.markdown(f"""
        <div class="sg-training-card">
            <p class="sg-training-title">{formation['nom']}</p>
            <p class="sg-training-meta">{formation['organisme']} · {formation['duree']} · comble : {formation['competence']}</p>
        </div>
        """, unsafe_allow_html=True)
