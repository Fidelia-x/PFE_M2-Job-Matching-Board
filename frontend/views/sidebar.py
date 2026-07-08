import streamlit as st

def render_sidebar(active_page: str):
    with st.sidebar:
        st.markdown("""
        <div class="sg-logo">
            <div class="sg-logo-dot"></div>
            <div class="sg-logo-text">SkillGap</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sg-nav-label">Navigation</div>', unsafe_allow_html=True)

        if st.button("Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button("Matching", key="nav_matching", use_container_width=True):
            st.session_state.page = "matching"
            st.rerun()

        for label in ["Mon CV", "Tendances", "Recommandations"]:
            st.markdown(f"""
            <div class="sg-nav-disabled">
                <span>{label}</span>
                <span class="sg-nav-badge">bientôt</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sg-sidebar-footer">', unsafe_allow_html=True)
        if st.button("Se déconnecter", key="logout_button_dashboard", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_prenom = None
            st.session_state.user_nom = None
            st.session_state.page = "accueil"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)