import streamlit as st

# st.write("J'ai chargé app.py")
def render_signup():
    # st.title("Connexion")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Séparation de l'écran en deux colonnes égales
    col_gauche, col_droite = st.columns([1, 1], gap="large")
    
    # --- COLONNE GAUCHE : FORMULAIRE ---
    with col_gauche:
        st.markdown("## Créez votre compte")
        
        # Bouton Google simulé
        st.button("🌐 Continuer avec Google", use_container_width=True, type="secondary")
        # st.markdown("<p style='text-align: center; color: grey; font-size: 0.8rem;'>ou</p>", unsafe_allow_html=True)
        st.markdown("""<div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 20px 0;
            color: #9aa0a6;
            font-weight: 600;
        ">
            <div style="flex: 1; height: 1px; background: #d9d9d9;"></div>
            <div>ou</div>
            <div style="flex: 1; height: 1px; background: #d9d9d9;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Champs Prénom et Nom côte à côte
        col_prenom, col_nom = st.columns(2)
        with col_prenom:
            prenom = st.text_input("Prénom", placeholder="Prénom")
        with col_nom:
            nom = st.text_input("Nom de famille", placeholder="Nom de famille")
            
        email = st.text_input("E-mail", placeholder="votre@email.com")
        password = st.text_input("Choisissez un mot de passe", type="password")
        
        # Case à cocher pour les conditions
        accepte_conditions = st.checkbox("J'accepte les conditions d'utilisation et la politique de confidentialité *")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Continuer", type="primary", use_container_width=True):
            if accepte_conditions and email and password:
                st.session_state.logged_in = True
                st.session_state.page = 'matching'
                st.rerun()
            else:
                st.error("Veuillez remplir les champs obligatoires et accepter les conditions.")
            
        col_txt1, col_btn = st.columns([8, 2])
        
        with col_txt1:
            st.markdown("<div style='text-align: left; color: #6c757d; padding-top: 9px;  font-size:0.9rem; margin-left: 180px;'>Vous avez déjà un compte ?</div>",unsafe_allow_html=True)
            

        st.markdown("""
            <style>
            .st-key-login_link button {
                background: none !important;
                border: none !important;
                color: #111827 !important;
                font-weight: 700 !important;
                text-decoration: underline !important;
                padding: 0 !important;
                box-shadow: none !important;
                margin-left: -195px;
            }
            .st-key-login_link button:hover {
                color: #4f46e5 !important;
                background: none !important;
            }
            </style>
        """, unsafe_allow_html=True) 
        with col_btn:
            if st.button("Connectez-vous", type='tertiary', key="login_link",use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()

    # --- COLONNE DROITE : ILLUSTRATION VISUELLE ---
    # with col_droite:
    #     # On utilise une boîte HTML/CSS pour faire le fond violet
    #     st.markdown(f"""
    #     <div class="illustration-box">
    #         <h2 style='color: white; margin-bottom: 20px;'>SkillGap AI</h2>
    #         <p style='font-size: 3.5rem; margin: 0;'>📄 ➔ 🤖 ➔ 🎯</p>
    #         <br>
    #         <p style='color: #E2D5E5; font-size: 1.1rem; max-width: 280px;'>
    #             Laissez notre modèle analyser votre CV et extraire vos compétences clés automatiquement.
    #         </p>
    #     </div>
    #     """, unsafe_allow_html=True)

def render_login():
    st.markdown("<br>", unsafe_allow_html=True)
    col_gauche, col_droite = st.columns([1.1, 1], gap="large")
    
    # --- COLONNE GAUCHE : FORMULAIRE DARK MODE ---
    with col_gauche:
        st.markdown("## Se connecter")
        
        # Bouton Google simulé
        st.button("🌐 Se connecter avec Google", use_container_width=True, type="secondary")
        st.markdown("""<div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 20px 0;
            color: #9aa0a6;
            font-weight: 600;
        ">
            <div style="flex: 1; height: 1px; background: #9aa0a6;"></div>
            <div>ou</div>
            <div style="flex: 1; height: 1px; background: #9aa0a6;"></div>
        </div>
        """, unsafe_allow_html=True)

        # Champ EMAIL
        st.markdown('<p class="dark-label">Email</p>', unsafe_allow_html=True)
        email = st.text_input("Email_hidden", placeholder="votre@email.com", label_visibility="collapsed")
        
        # Champ MOT DE PASSE
        st.markdown('<p class="dark-label">Mot de passe</p>', unsafe_allow_html=True)
        password = st.text_input("Pass_hidden", type="password", label_visibility="collapsed")
        
        # Options : Se souvenir de moi & Mot de passe oublié
        col_opt1, col_opt2 = st.columns([4, 1])
        st.markdown("""
        <style>
        .st-key-forgot_pass button {
            background: none !important;
            border: none !important;
            padding: 0 !important;
            color: #111827 !important;
            font-weight: 700 !important;
            text-decoration: underline !important;
            box-shadow: none !important;
            padding: 0 !important;        
        }
        .st-key-forgot_pass button:hover {
            color: #4f46e5 !important;
            background: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        with col_opt2:
            if st.button("Mot de passe oublié ?", type='tertiary', key="forgot_pass"):
                st.toast("Lien de récupération envoyé !")
                    
        # Bouton de soumission principal
        if st.button("Se connecter", type="primary", use_container_width=True):
            if email and password:
                st.session_state.logged_in = True
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("Veuillez remplir tous les champs.")
                            
        # Lien d'inscription tout en bas (sur une seule ligne et souligné au survol)
        col_txt1, col_btn = st.columns([5, 3])
        with col_txt1:
            st.markdown("<div style='text-align: left; color: #6c757d; padding-top: 9px;  font-size:0.9rem; margin-left: 210px;'>Pas encore de compte ?</div>",unsafe_allow_html=True)

        st.markdown("""
            <style>
            .st-key-login_link button {
                background: none !important;
                border: none !important;
                color: #111827 !important;
                font-weight: 700 !important;
                text-decoration: underline !important;
                padding: 0 !important;
                box-shadow: none !important;
                margin-left: -165px;
            }
            .st-key-login_link button:hover {
                color: #4f46e5 !important;
                background: none !important;
            }
            </style>
        """, unsafe_allow_html=True) 
        with col_btn:
            if st.button("Inscrivez vous", type='tertiary', key="login_link",use_container_width=True):
                st.session_state.page = 'signup'
                st.rerun()
                

        st.markdown('</span></div>', unsafe_allow_html=True)

    # --- COLONNE DROITE : ILLUSTRATION ---
    # with col_droite:
    #     st.markdown(f"""
    #     <div class="illustration-box-dark">
    #         <h2 style='color: white; margin-bottom: 10px; font-weight: 700;'>SkillGap AI</h2>
    #         <p style='color: #A78BFA; font-size: 1.1rem;'>L'intelligence artificielle au service de votre carrière.</p>
    #         <br>
    #         <p style='font-size: 4rem; margin: 20px 0;'>✨🤖🎯</p>
    #         <br>
    #         <p style='color: #7C7C8A; font-size: 0.9rem; max-width: 260px;'>
    #             Connectez-vous pour analyser instantanément vos compétences par rapport aux attentes du marché.
    #         </p>
    #     </div>
    #     """, unsafe_allow_html=True)