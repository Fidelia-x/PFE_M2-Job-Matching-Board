import streamlit as st
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header

def render_dashboard():
    inject_dashboard_style()
    render_sidebar(active_page="dashboard")
    render_header(subtitle="Voici votre tableau de bord")

    st.markdown("""
    <div class="sg-placeholder-wrap">
        <div class="sg-pulse"></div>
        <p class="sg-placeholder-title">Cette section arrive bientôt</p>
        <p class="sg-placeholder-sub">
            On construit ton tableau de bord. Reviens un peu plus tard.
        </p>
    </div>
    """, unsafe_allow_html=True)