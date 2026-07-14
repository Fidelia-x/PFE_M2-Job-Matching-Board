import streamlit as st
# from airflow_client import airflow
from scripts.matching_cv import find_best_matches
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header
from back_service.cv_parser import extract_cv_text
# Radar de compétences : pas encore de backend d'extraction de compétences /
# calcul d'écart réel, donc désactivé pour l'instant (voir _render_skill_gap_results
# plus bas, laissé en commentaire pour reprise future).
# from views.svg_charts import radar_chart_svg, gauge_svg
# from views.mock_data import get_mock_skill_gap


def render_matching():
    inject_dashboard_style()
    render_sidebar(active_page="matching")
    render_header(subtitle="Analysez votre CV pour voir votre correspondance", title="Matching")

    if st.session_state.get("matching_done"):
        _render_matching_results(st.session_state.matched_offers)
        if st.button("← Lancer une nouvelle analyse", key="restart_matching"):
            st.session_state.matching_done = False
            st.rerun()
        return

    _render_dropzone()

    with st.expander("Options avancées : coller le texte du CV (pour tester sans fichier)"):
        cv_text = st.text_area("Collez le texte de votre CV ici", height=200)
        if st.button("Analyser ce texte", key="analyze_pasted_text"):
            if not cv_text.strip():
                st.warning("Collez d'abord le texte de votre CV.")
            else:
                _run_matching(cv_text)


def _render_dropzone():
    with st.container(key="cv_dropzone"):
        st.markdown("""
        <div class="sg-dropzone-icon">📄</div>
        <p class="sg-dropzone-title">Glissez votre CV ici</p>
        <p class="sg-dropzone-sub">Formats PDF ou DOCX — analyse automatique de vos compétences</p>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("CV", type=["pdf", "docx"], label_visibility="collapsed", key="cv_upload")

        col_l, col_mid, col_r = st.columns([1, 1, 1])
        with col_mid:
            if st.button("Lancer le matching", key="launch_matching", use_container_width=True):
                if uploaded_file is None:
                    st.warning("Déposez d'abord votre CV (PDF ou DOCX).")
                else:
                    with st.spinner("Lecture du CV..."):
                        try:
                            cv_text = extract_cv_text(uploaded_file)
                        except ValueError as e:
                            st.error(str(e))
                            return
                    _run_matching(cv_text)


def _run_matching(cv_text):
    with st.spinner("Analyse en cours..."):
        try:
            results = find_best_matches(cv_text, top_n=20)
        except Exception as e:
            st.error(f"Erreur lors du matching : {e}")
            return

    st.session_state.cv_text = cv_text
    st.session_state.matched_offers = results
    st.session_state.matching_done = True
    st.rerun()


def _format_salaire(mn, mx):
    def valid(v):
        return v is not None and v >= 0

    mn = mn if valid(mn) else None
    mx = mx if valid(mx) else None

    def fmt(v):
        return f"{v / 1000:.0f}k€" if v >= 1000 else f"{v:.0f}€"

    if mn is not None and mx is not None:
        return f"{fmt(mn)} – {fmt(mx)}"
    if mn is not None or mx is not None:
        return fmt(mn if mn is not None else mx)
    return "Salaire non précisé"


def _render_matching_results(offers):
    st.markdown('<div class="sg-section-title">Résultat de l\'analyse</div>', unsafe_allow_html=True)

    if not offers:
        st.info("Aucune offre correspondante trouvée pour le moment. Réessayez plus tard, de nouvelles offres sont ajoutées régulièrement.")
        return

    top_score = round(offers[0]["score"] * 100)
    st.markdown('<div class="sg-kpi-row">', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sg-kpi">
            <div class="sg-kpi-label">Offres correspondantes</div>
            <div class="sg-kpi-value">{len(offers)}</div>
        </div>
        <div class="sg-kpi">
            <div class="sg-kpi-label">Meilleure correspondance</div>
            <div class="sg-kpi-value">{top_score}%</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sg-section-title">Offres les plus proches de votre profil</div>', unsafe_allow_html=True)
    for offre in offers[:5]:
        url = offre.get("source_url")
        tag_open = f'<a class="sg-offer-card" href="{url}" target="_blank" rel="noopener noreferrer">' if url else '<div class="sg-offer-card">'
        tag_close = "</a>" if url else "</div>"
        st.markdown(f"""
        {tag_open}
            <div>
                <p class="sg-offer-title">{offre['titre']}</p>
                <p class="sg-offer-meta">{offre['company']} · {offre.get('localisation') or 'Lieu non précisé'} · {offre.get('contract') or 'Contrat non précisé'} · {_format_salaire(offre.get('salaire_min'), offre.get('salaire_max'))}</p>
            </div>
            <div>
                <div class="sg-offer-score">{round(offre['score'] * 100)}%</div>
                <div class="sg-offer-score-label">Correspondance</div>
            </div>
        {tag_close}
        """, unsafe_allow_html=True)

    if st.button("Voir toutes les offres →", key="go_to_offres"):
        st.session_state.page = "offres"
        st.rerun()


# --- Radar de compétences (désactivé : nécessite un vrai backend d'extraction
# de compétences + calcul d'écart, pas seulement le matching par similarité
# globale de find_best_matches). À reprendre quand ce backend existera. ---
#
# _PILL_CLASS = {"success": "sg-pill-success", "warning": "sg-pill-warning", "danger": "sg-pill-danger"}
# _PILL_LABEL = {"success": "Acquise", "warning": "À développer", "danger": "Critique"}
#
# def _render_skill_gap_results(data):
#     st.markdown('<div class="sg-section-title">Résultat de l\'analyse</div>', unsafe_allow_html=True)
#
#     col_radar, col_gauge = st.columns([2, 1])
#     with col_radar:
#         st.markdown('<div class="sg-card">', unsafe_allow_html=True)
#         st.markdown(
#             radar_chart_svg(
#                 [s["name"] for s in data["skills"]],
#                 [s["current"] for s in data["skills"]],
#                 [s["target"] for s in data["skills"]],
#             ),
#             unsafe_allow_html=True,
#         )
#         st.markdown('</div>', unsafe_allow_html=True)
#     with col_gauge:
#         st.markdown('<div class="sg-card">', unsafe_allow_html=True)
#         st.markdown(gauge_svg(data["score"], label="Correspondance au poste"), unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)
#
#     st.markdown('<div class="sg-kpi-row">', unsafe_allow_html=True)
#     st.markdown(f"""
#         <div class="sg-kpi">
#             <div class="sg-kpi-label">Score global</div>
#             <div class="sg-kpi-value">{data['score']}%</div>
#         </div>
#         <div class="sg-kpi">
#             <div class="sg-kpi-label">Compétences acquises</div>
#             <div class="sg-kpi-value">{len(data['acquired'])}</div>
#         </div>
#         <div class="sg-kpi">
#             <div class="sg-kpi-label">Écarts à combler</div>
#             <div class="sg-kpi-value">{len(data['to_develop'])}</div>
#         </div>
#     """, unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)
#
#     col_ok, col_todo = st.columns(2)
#     with col_ok:
#         st.markdown('<div class="sg-section-title">Compétences maîtrisées</div>', unsafe_allow_html=True)
#         pills = "".join(f'<span class="sg-pill sg-pill-success">{name}</span> ' for name in data["acquired"]) or \
#             '<span class="sg-pill sg-pill-warning">Aucune pour le moment</span>'
#         st.markdown(pills, unsafe_allow_html=True)
#     with col_todo:
#         st.markdown('<div class="sg-section-title">Compétences à développer</div>', unsafe_allow_html=True)
#         pills = "".join(
#             f'<span class="sg-pill {_PILL_CLASS[s["status"]]}">{s["name"]}</span> ' for s in data["to_develop"]
#         ) or '<span class="sg-pill sg-pill-success">Tout est acquis 🎉</span>'
#         st.markdown(pills, unsafe_allow_html=True)
#
#     st.markdown('<div class="sg-section-title">Détail par compétence</div>', unsafe_allow_html=True)
#     rows = "".join(
#         f"""<tr>
#             <td>{s['name']}</td>
#             <td>{s['current']}%</td>
#             <td>{s['target']}%</td>
#             <td>{'+' if s['gap'] < 0 else ''}{-s['gap']}%</td>
#             <td><span class="sg-pill {_PILL_CLASS[s['status']]}">{_PILL_LABEL[s['status']]}</span></td>
#         </tr>"""
#         for s in data["skills"]
#     )
#     st.markdown(f"""
#     <table class="sg-table">
#         <thead><tr><th>Compétence</th><th>Niveau actuel</th><th>Niveau cible</th><th>Écart</th><th>Statut</th></tr></thead>
#         <tbody>{rows}</tbody>
#     </table>
#     """, unsafe_allow_html=True)
#
#     st.markdown(f"""
#     <div class="sg-banner">
#         <div class="sg-banner-text">
#             <strong>{len(data['to_develop'])} compétence(s)</strong> à combler pour matcher pleinement le poste cible.
#             Découvrez des formations ciblées dans Recommandations.
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
#     if st.button("Voir les recommandations →", key="go_to_recommendation"):
#         st.session_state.page = "recommendation"
#         st.rerun()
