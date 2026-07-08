import streamlit as st
# from airflow_client import airflow
from scripts.matching_cv import find_best_matches
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header

def render_matching():
    inject_dashboard_style()
    render_sidebar(active_page="matching")
    render_header(subtitle="Trouvez vos meilleures opportunités", title="Matching")

    st.markdown("---")
    st.info("Soumettez votre CV (texte) puis lancez le pipeline si vous voulez rafraîchir les offres.")
    cv_text = st.text_area("Collez le texte de votre CV ici", height=200)
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Lancer le pipeline Airflow puis analyser"):
            # ... ton code existant inchangé ...
            pass

    with col2:
        if st.button("Analyser mon CV (sans relancer Airflow)"):
            if not cv_text.strip():
                st.warning("Collez d'abord le texte de votre CV.")
            else:
                with st.spinner("Analyse en cours..."):
                    try:
                        results = find_best_matches(cv_text, top_n=5)
                        if not results:
                            st.info("Aucun résultat trouvé — vérifiez que la table `offres_emploi` est remplie.")
                        else:
                            for r in results:
                                st.markdown(f"**{r['titre']}** — {r['company']} (score: {r['score']})")
                    except Exception as e:
                        st.error(f"Erreur lors du matching : {e}")