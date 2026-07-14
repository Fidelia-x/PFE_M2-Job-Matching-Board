import streamlit as st


def require_matching(button_key="go_to_matching"):
    """Affiche un écran de rappel si l'utilisateur n'a pas encore lancé de matching CV.
    Retourne True si la page appelante peut afficher son contenu, False sinon."""
    if st.session_state.get("matching_done"):
        return True

    st.markdown("""
    <div class="sg-gate-wrap">
        <p class="sg-gate-title">Lancez d'abord une analyse de CV</p>
        <p class="sg-gate-sub">
            Cette section se remplit avec vos résultats une fois le matching CV effectué.
            Rendez-vous sur "Matching CV" pour déposer votre CV et lancer l'analyse.
        </p>
    </div>
    """, unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("Aller à Matching CV", key=button_key, use_container_width=True):
            st.session_state.page = "matching"
            st.rerun()
    return False
