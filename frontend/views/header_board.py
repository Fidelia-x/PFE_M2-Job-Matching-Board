import streamlit as st
from styles.dashbord_style import inject_dashboard_style

def render_header(subtitle: str = "", title: str = None):
    prenom = st.session_state.get("user_prenom", "")
    greeting = f"Bonjour {prenom} 👋" if prenom else "Bonjour 👋"
    display_title = title if title else greeting
    initiales = prenom[0].upper() if prenom else "?"

    st.markdown(f"""
    <div class="sg-header">
        <div>
            <p class="sg-header-greeting">{display_title}</p>
            <p class="sg-header-sub">{subtitle}</p>
        </div>
        <div class="sg-header-right">
            <div class="sg-search">Rechercher...</div>
            <div class="sg-bell">🔔</div>
            <div class="sg-avatar">{initiales}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)