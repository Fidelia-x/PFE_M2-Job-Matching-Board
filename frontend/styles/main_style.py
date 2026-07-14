import streamlit as st

def inject_main_style():
    st.markdown("""
<style>
    /* 1. Bouton secondaire ("Se connecter") -> Devient brun foncé au survol */
    div.stButton > button[kind="secondary"] {
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #2B2620 !important;
        color: white !important;
        border-color: #2B2620 !important;
        box-shadow: 0px 4px 12px rgba(43, 38, 32, 0.15);
        transform: translateY(-1px);
    }

    /* 2. Bouton primaire ("Essayer maintenant" / "Confirmer") -> Devient brun foncé au survol */
    div.stButton > button[kind="primary"] {
        background-color: #B5654A;
        border-color: #B5654A;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #2B2620 !important;
        color: white !important;
        border-color: #2B2620 !important;
        box-shadow: 0px 4px 12px rgba(43, 38, 32, 0.25);
        transform: translateY(-1px);
    }
    .illustration-box {
        background-color: #7A4432; /* Terracotta foncé assorti à la palette */
        border-radius: 12px;
        padding: 40px;
        color: white;
        text-align: center;
        min-height: 480px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)