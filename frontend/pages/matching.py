import streamlit as st
# from airflow_client import airflow
from scripts.matching_cv import find_best_matches

def render_matching():
    st.title("🚀 Mon espace Matching")

    st.markdown("---")
    st.info("Soumettez votre CV (texte) puis lancez le pipeline si vous voulez rafraîchir les offres.")

    cv_text = st.text_area("Collez le texte de votre CV ici", height=200)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Lancer le pipeline Airflow puis analyser"):
            dag_id = st.text_input("DAG id", value='master_pipeline_full_workflow')
            try:
                # Déclenche le DAG
                run = airflow.trigger_dag(dag_id)
                run_id = run.get('dag_run_id') or run.get('dag_run', {}).get('dag_run_id')
                if not run_id:
                    st.warning("DAG déclenché mais aucun run_id reçu — vérifiez Airflow.")
                else:
                    with st.spinner(f"DAG déclenché (run {run_id}). Attente de la fin..."):
                        # Polling simple — adapte poke_interval et timeout selon tes besoins
                        import time
                        status = None
                        for _ in range(120):
                            info = airflow.get_dag_run(dag_id, run_id)
                            status = info.get('state')
                            if status in ('success', 'failed'):
                                break
                            time.sleep(5)
                        st.success(f"DAG terminé avec état: {status}")
                        if status != 'success':
                            st.error('Le DAG a échoué ou n\'a pas retourné success. Vérifiez Airflow.')
            except Exception as e:
                st.error(f"Erreur en déclenchant le DAG: {e}")

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

    st.markdown("---")
    if st.button("Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.page = 'accueil'
        st.rerun()