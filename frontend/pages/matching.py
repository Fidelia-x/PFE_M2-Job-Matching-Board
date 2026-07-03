import streamlit as st

def render_matching():
    st.title("🚀 Mon espace Dashboard")
    # Ici, tout ton code de matching et d'analyse avec Mistral
    if st.button("Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.page = 'accueil'
        st.rerun()