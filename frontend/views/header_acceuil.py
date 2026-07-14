import streamlit as st

# --- HEADER (Isolé à part) ---
def render_header():
    col1, col2 = st.columns([6, 2])
    
    with col1:
        if st.button("SkillGap", type="tertiary"):
            st.session_state.page = 'accueil'
            st.rerun()
            
    with col2:
        is_login = st.session_state.page == 'login'
        # Le bouton de connexion bascule sur le style primaire ou secondaire selon la page active
        if st.button("Se connecter", type="primary" if is_login else "secondary", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()

def render_accueil():
    render_header()
    # st.title("🎯 Bienvenue sur SkillGap AI")

    st.markdown("<br><br>", unsafe_allow_html=True) 
    st.markdown("<h1 style='text-align: center;'>Trouvez le match parfait en quelques secondes.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7A7266; font-size: 1.2rem;'>Uploadez votre CV, notre IA analyse vos compétences et vous connecte aux meilleures opportunités.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True) 
    
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_b:
        if st.button("Essayer maintenant", type="primary", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()    