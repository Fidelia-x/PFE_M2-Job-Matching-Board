import streamlit as st

# st.write("J'ai chargé pppppppppppppppp.py")
def render_dashboard():
    st.write("### Bienvenue sur ton Dashboard")
    st.info("Ceci est le contenu spécifique au tableau de bord.")

if st.sidebar.button("Se déconnecter"):
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.page = 'accueil'
    st.rerun()