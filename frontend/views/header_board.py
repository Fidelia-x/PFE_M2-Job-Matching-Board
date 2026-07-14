import streamlit as st
from styles.dashbord_style import inject_dashboard_style

def render_header(subtitle: str = "", title: str = None):
    prenom = st.session_state.get("user_prenom", "")
    greeting = f"Bonjour {prenom} 👋" if prenom else "Bonjour 👋"
    display_title = title if title else greeting
    initiales = prenom[0].upper() if prenom else "?"

    with st.container(key="sg_header_row"):
        col_title, col_search, col_bell, col_avatar = st.columns(
            [5, 2, 0.6, 0.6], vertical_alignment="center"
        )
        with col_title:
            st.markdown(f"""
            <div>
                <p class="sg-header-greeting">{display_title}</p>
                <p class="sg-header-sub">{subtitle}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_search:
            st.markdown('<div class="sg-search">Rechercher...</div>', unsafe_allow_html=True)
        with col_bell:
            st.markdown('<div class="sg-bell">🔔</div>', unsafe_allow_html=True)
        with col_avatar:
            st.markdown(f'<div class="sg-avatar">{initiales}</div>', unsafe_allow_html=True)