import streamlit as st

def inject_main_style():
    st.markdown("""
<style>
    /* 1. Bouton secondaire ("Se connecter") -> Devient noir au survol */
    div.stButton > button[kind="secondary"] {
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #1A1A1A !important; 
        color: white !important;               
        border-color: #1A1A1A !important;       
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15); 
        transform: translateY(-1px);
    }

    /* 2. Bouton primaire ("Essayer maintenant" / "Confirmer") -> Devient noir au survol */
    div.stButton > button[kind="primary"] {
        background-color: #FF4B4B; 
        border-color: #FF4B4B;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1A1A1A !important; 
        color: white !important;               
        border-color: #1A1A1A !important;       
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.25); 
        transform: translateY(-1px);
    }
    .illustration-box {
        background-color: #2D0C33; /* Violet foncé similaire à ton image */
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