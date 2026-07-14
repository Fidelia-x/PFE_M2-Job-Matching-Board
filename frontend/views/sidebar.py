import streamlit as st

# Fait correspondre la valeur de st.session_state.page (source de vérité pour le
# routing dans app.py) à la clé du bouton de nav correspondant, pour que le
# surlignage de la page active ne dépende pas d'une chaîne passée à la main par
# chaque page (source d'un bug précédent : orthographes différentes).
_PAGE_TO_NAV_KEY = {
    "matching": "nav_matching",
    "offres": "nav_offres",
    "tendences": "nav_tendences",
    "recommendation": "nav_recommandations",
    "assistant_ia": "nav_assistant",
    "guide_conception": "nav_guide_conception",
}

def render_sidebar(active_page: str = None):
    active_key = _PAGE_TO_NAV_KEY.get(st.session_state.get("page"), "")
    with st.sidebar:
        st.markdown(f"""
        <style>
        .st-key-{active_key} button,
        .st-key-{active_key} button:hover,
        .st-key-{active_key} button:focus,
        .st-key-{active_key} button:focus:not(:active),
        .st-key-{active_key} button:active {{
            background: var(--accent-dim) !important;
            color: var(--accent) !important;
            border-color: transparent !important;
            box-shadow: none !important;
        }}
        .st-key-{active_key} button *,
        .st-key-{active_key} button:hover *,
        .st-key-{active_key} button:focus *,
        .st-key-{active_key} button:active * {{
            color: var(--accent) !important;
        }}
        </style>
        <div class="sg-logo">
            <div class="sg-logo-dot"></div>
            <div class="sg-logo-text">SkillGap</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sg-nav-label">Navigation</div>', unsafe_allow_html=True)
        

        if st.button("🔍 Matching CV", key="nav_matching", use_container_width=True):
            st.session_state.page = "matching"
            st.rerun()

        if st.button("💼 Offres trouvées", key="nav_offres", use_container_width=True):
            st.session_state.page = "offres"
            st.rerun()

        if st.button("📈 Tendences du marchés", key="nav_tendences", use_container_width=True):
            st.session_state.page = "tendences"
            st.rerun()

        if st.button("✨ Recommandations", key="nav_recommandations", use_container_width=True):
            st.session_state.page = "recommendation"
            st.rerun()

        if st.button("💬 Assistant IA", key="nav_assistant", use_container_width=True):
            st.session_state.page = "assistant_ia"
            st.rerun()

        # if st.button("📘 Guide de conception", key="nav_guide_conception", use_container_width=True):
        #     st.session_state.page = "guide_conception"
        #     st.rerun()

        with st.container(key="sg_sidebar_footer"):
            prenom = st.session_state.get("user_prenom", "")
            nom = st.session_state.get("user_nom", "")
            nom_complet = f"{prenom} {nom}".strip() or "Mon profil"

            with st.popover(f"👤 {nom_complet}", use_container_width=True):
                st.markdown('<div class="sg-popover-label">Compte</div>', unsafe_allow_html=True)
                st.button("⚙️ Paramètres", use_container_width=True, key="profile_settings")
                st.selectbox("Langue", ["Français", "English"], key="profile_lang", label_visibility="collapsed")

                st.markdown('<div class="sg-popover-label">Apparence</div>', unsafe_allow_html=True)
                dark_mode = st.toggle("Mode sombre", value=st.session_state.get("dark_mode", False), key="dark_mode_toggle")
                if dark_mode != st.session_state.get("dark_mode", False):
                    st.session_state.dark_mode = dark_mode
                    st.rerun()

                st.markdown('<div class="sg-popover-label">&nbsp;</div>', unsafe_allow_html=True)
                if st.button("🚪 Déconnexion", use_container_width=True, key="logout_button_dashboard"):
                    st.session_state.logged_in = False
                    st.session_state.user_id = None
                    st.session_state.user_prenom = None
                    st.session_state.user_nom = None
                    st.session_state.matching_done = False
                    st.session_state.page = "accueil"
                    st.rerun()