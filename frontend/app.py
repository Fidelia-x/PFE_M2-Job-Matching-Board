import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import importlib
import pages.authentification
import pages.header_acceuil
import pages.dashboard
import pages.matching
import styles.main_style

importlib.reload(pages.authentification)
importlib.reload(pages.header_acceuil)
importlib.reload(pages.dashboard)
importlib.reload(pages.matching)
importlib.reload(styles.main_style)

from styles.main_style import inject_main_style
from pages.header_acceuil import render_accueil
from pages.authentification import render_login, render_signup
from pages.dashboard import render_dashboard
from pages.matching import render_matching
from back_service.gestion_table_user import init_db


# Configuration de la page
# st.set_page_config(page_title="SkillGap", layout="centered")
st.set_page_config(page_title="SkillGap", layout="wide")

#code css
inject_main_style()

@st.cache_resource
def init_db_once():
    init_db()
    return True

init_db_once()

# --- INITIALISATION DE LA NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'accueil'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIQUE DE NAVIGATION ---
def show_page():
    # Protection : si l'utilisateur n'est pas connecté et essaie d'accéder au dashboard/matching
    if not st.session_state.logged_in:
        if st.session_state.page == 'signup':
            render_signup()
        elif st.session_state.page == 'login':
            render_login()
        else:
            render_accueil() # Par défaut, accueil pour les non-connectés
    else:
        # Zone connectée
        if st.session_state.page == 'dashboard':
            render_dashboard()
        elif st.session_state.page == 'matching':
            render_matching()
        else:
            render_dashboard() # Page par défaut après login


show_page()