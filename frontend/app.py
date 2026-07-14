import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import importlib
import styles.main_style
import styles.dashbord_style
import views.authentification
import views.header_acceuil
import views.offres
import views.matching
import views.tendences
import views.recommendation
import views.assistant_ia

# Les modules de style sont rechargés en premier : les vues font
# `from styles.xxx import ...` à l'import, donc si on les recharge après les
# vues, ces dernières gardent la fonction figée de la toute première exécution
# du process (le cache de sys.modules n'est pas rafraîchi par runOnSave).
importlib.reload(styles.main_style)
importlib.reload(styles.dashbord_style)
importlib.reload(views.authentification)
importlib.reload(views.header_acceuil)
importlib.reload(views.offres)
importlib.reload(views.matching)
importlib.reload(views.tendences)
importlib.reload(views.recommendation)
importlib.reload(views.assistant_ia)

from styles.main_style import inject_main_style
from views.header_acceuil import render_accueil
from views.authentification import render_login, render_signup
from views.offres import render_offres
from views.matching import render_matching
from views.recommendation import render_recommendation
from views.assistant_ia import render_assistant_ia
from views.tendences import render_tendences
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
if 'matching_done' not in st.session_state:
    st.session_state.matching_done = False
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

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
        if st.session_state.page == 'offres':
            render_offres()
        elif st.session_state.page == 'matching':
            render_matching()
        elif st.session_state.page == 'tendences':
            render_tendences()
        elif st.session_state.page == 'recommendation':
            render_recommendation()
        elif st.session_state.page == 'assistant_ia':
            render_assistant_ia()
        else:
            render_matching() # Page par défaut après login


show_page()