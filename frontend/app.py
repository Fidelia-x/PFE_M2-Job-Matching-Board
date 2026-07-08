import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import importlib
import views.authentification
import views.header_acceuil
import views.dashboard
import views.matching
import styles.main_style

importlib.reload(views.authentification)
importlib.reload(views.header_acceuil)
importlib.reload(views.dashboard)
importlib.reload(views.matching)
importlib.reload(styles.main_style)

from styles.main_style import inject_main_style
from views.header_acceuil import render_accueil
from views.authentification import render_login, render_signup
from views.dashboard import render_dashboard
from views.matching import render_matching
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