import math

import streamlit as st
# from airflow_client import airflow
from scripts.matching_cv import find_best_matches, get_market_fit_stats, rank_missing_skills
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header
from back_service.cv_parser import extract_cv_text, extract_target_role
from views.offer_card import render_offer_card
from scripts.training_catalog import get_trainings_for_skill
from views.recommendation import MAX_SKILLS as RECOMMENDATION_SKILLS_COUNT

# Nombre de compétences affichées dans "Quoi apprendre en priorité" — même
# esprit que MAX_SKILLS dans la page Recommandations, mais volontairement
# plus court ici : c'est un teaser sur la page Matching, pas la liste complète.
PRIORITY_SKILLS_COUNT = 3
# Radar de compétences : pas encore de backend d'extraction de compétences /
# calcul d'écart réel, donc désactivé pour l'instant (voir _render_skill_gap_results
# plus bas, laissé en commentaire pour reprise future).
# from views.svg_charts import radar_chart_svg, gauge_svg


def render_matching():
    inject_dashboard_style()
    render_sidebar(active_page="matching")
    render_header(subtitle="Analysez votre CV pour voir votre correspondance", title="Matching")

    if st.session_state.get("matching_done"):
        _render_matching_results(st.session_state.matched_offers)
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
                    _run_matching(cv_text, filename=uploaded_file.name)


@st.cache_data(ttl=600, show_spinner=False)
def _cached_market_fit_stats(cv_text):
    return get_market_fit_stats(cv_text)


def _tension_label(pct):
    if pct >= 15:
        return "Profil très demandé"
    if pct >= 5:
        return "Demande modérée"
    return "Profil de niche"


def _run_matching(cv_text, filename=None):
    with st.spinner("Analyse en cours..."):
        try:
            results = find_best_matches(cv_text, top_n=50)
        except Exception as e:
            st.error(f"Erreur lors du matching : {e}")
            return

    st.session_state.cv_text = cv_text
    st.session_state.cv_filename = filename
    st.session_state.cv_target_role = extract_target_role(cv_text)
    st.session_state.matched_offers = results
    st.session_state.matching_done = True
    st.session_state.offres_display_count = 20
    # Le contexte du profil affiché par l'Assistant IA change à chaque nouveau
    # matching — sans ça, une nouvelle analyse garderait l'ancienne
    # conversation avec un contexte devenu obsolète.
    st.session_state.chat_messages = []
    st.rerun()


def _top_missing_skill(offers):
    ranked = rank_missing_skills(offers)
    return ranked[0] if ranked else None


def _score_ring_svg(pct, size=84, stroke_width=8):
    """Anneau de progression en SVG pur (stroke-dasharray) plutôt qu'un
    graphique Altair : c'est un simple indicateur intégré dans une tuile KPI,
    pas un chart autonome, donc pas besoin de la machinerie Vega-Lite pour
    ça."""
    radius = (size - stroke_width) / 2
    circumference = 2 * math.pi * radius
    offset = circumference * (1 - pct / 100)
    center = size / 2
    # Une seule ligne, sans retour ni indentation : injecté tel quel dans le
    # f-string appelant, un simple `\n` en tête suffit à casser le bloc HTML
    # de Markdown (voir dedent() dans tendences.py pour le même piège) — tout
    # ce qui suit serait alors rendu comme texte brut au lieu d'être interprété.
    return (
        f'<div class="sg-ring-wrap"><svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'<circle class="sg-ring-track" cx="{center}" cy="{center}" r="{radius}" fill="none" stroke-width="{stroke_width}"/>'
        f'<circle class="sg-ring-progress" cx="{center}" cy="{center}" r="{radius}" fill="none" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}" '
        f'transform="rotate(-90 {center} {center})"/>'
        f'<text class="sg-ring-value" x="{center}" y="{center}" text-anchor="middle" dominant-baseline="central">{pct}%</text>'
        f'</svg></div>'
    )


def _render_priority_learning(offers):
    """"Quoi apprendre en priorité" : les compétences manquantes les plus
    fréquentes dans les offres matchées, avec un lien direct vers une
    formation du catalogue.

    "Points de correspondance estimés" est une estimation illustrative
    (pct d'offres où la compétence manque, ramené à une échelle de points),
    pas une simulation exacte de l'effet sur le score — on n'a pas de moyen
    fiable de recalculer le score sans cette compétence sans ré-encoder le
    CV pour chaque hypothèse."""
    top_gaps = rank_missing_skills(offers)[:PRIORITY_SKILLS_COUNT]
    if not top_gaps:
        return

    with st.container(border=True):
        st.markdown("""
        <div class="sg-context-title">Quoi apprendre en priorité</div>
        <div class="sg-chat-sub">Classé par impact sur votre score de correspondance</div>
        """, unsafe_allow_html=True)

        for i, (skill, pct) in enumerate(top_gaps):
            points = max(1, round(pct / 5))
            with st.container(key=f"priority_row_{i}"):
                col_info, col_btn = st.columns([3, 1])
                with col_info:
                    st.markdown(f"""
                    <p class="sg-training-title">{skill}</p>
                    <p class="sg-training-meta">+{points} points de correspondance estimés</p>
                    """, unsafe_allow_html=True)
                with col_btn:
                    trainings = get_trainings_for_skill(skill)
                    if trainings:
                        st.link_button("Voir la formation", trainings[0]["lien"], use_container_width=True)


def _render_recommendation_banner(offers):
    gap_count = min(len(rank_missing_skills(offers)), RECOMMENDATION_SKILLS_COUNT)
    if not gap_count:
        return

    with st.container(key="reco_banner"):
        col_text, col_btn = st.columns([3, 1])
        with col_text:
            st.markdown(f"""
            <div class="sg-banner-text">
                <strong>✨ Des recommandations vous attendent</strong><br>
                {gap_count} formation(s) suggérée(s) pour combler vos écarts prioritaires.
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            if st.button("Voir les recommandations", key="go_to_recommendation", type="primary", use_container_width=True):
                st.session_state.page = "recommendation"
                st.rerun()


def _render_matching_results(offers):
    col_title, col_restart = st.columns([4, 1])
    with col_title:
        st.markdown('<div class="sg-section-title">Résultat de l\'analyse</div>', unsafe_allow_html=True)
    with col_restart:
        if st.button("↻ Recommencer l'analyse", key="restart_matching", use_container_width=True):
            st.session_state.matching_done = False
            st.rerun()

    if not offers:
        st.info("Aucune offre correspondante trouvée pour le moment. Réessayez plus tard, de nouvelles offres sont ajoutées régulièrement.")
        return

    top_score = round(offers[0]["score"] * 100)
    # round() plutôt que comparer le score brut à 0.70 : sinon une offre à
    # 69.6% s'affiche "70%" dans l'anneau juste à côté mais ne compte pas
    # comme compatible, ce qui a l'air incohérent pour l'utilisateur.
    compatible_count = sum(1 for o in offers if round(o["score"] * 100) >= 70)
    top_missing = _top_missing_skill(offers)
    # "Taux d'éligibilité immédiate" désactivé pour l'instant (voir demande) —
    # laissé en commentaire pour reprise future plutôt que supprimé. Ça reste
    # la seule utilisation de market_fit, donc son calcul (requête marché +
    # ré-encodage du CV) est aussi commenté pour ne pas tourner pour rien.
    # market_fit = _cached_market_fit_stats(st.session_state.cv_text)

    top_missing_tile = ""
    if top_missing:
        skill_name, skill_pct = top_missing
        top_missing_tile = f"""
        <div class="sg-kpi sg-kpi-center">
            <div class="sg-kpi-label">Compétence à acquérir en priorité</div>
            <div class="sg-kpi-value-danger">{skill_name}</div>
            <div class="sg-kpi-sub">demandée dans {skill_pct}% des offres</div>
        </div>"""

    st.markdown(f"""
        <div class="sg-kpi-row">
            <div class="sg-kpi">
                <div class="sg-kpi-label">Meilleure correspondance</div>
                {_score_ring_svg(top_score)}
                <div class="sg-kpi-sub sg-kpi-sub-center">avec une offre du marché</div>
            </div>
            <div class="sg-kpi sg-kpi-center">
                <div class="sg-kpi-label">Offres compatibles</div>
                <div class="sg-kpi-value">{compatible_count}</div>
                <div class="sg-kpi-sub">score de correspondance &ge; 70%</div>
            </div>{top_missing_tile}
        </div>
    """, unsafe_allow_html=True)

    # "Taux d'éligibilité immédiate" désactivé pour l'instant (voir demande) —
    # laissé en commentaire pour reprise future plutôt que supprimé.
    # st.markdown('<div class="sg-kpi-row">', unsafe_allow_html=True)
    # st.markdown(f"""
    #     <div class="sg-kpi">
    #         <div class="sg-kpi-label">Taux d'éligibilité immédiate</div>
    #         <div class="sg-kpi-value">{market_fit['eligibility_rate']}%</div>
    #         <div class="sg-kpi-sub">des offres du marché avec un score &gt; 70%</div>
    #     </div>
    # """, unsafe_allow_html=True)
    # "Indice de tension du profil" désactivé pour l'instant (voir demande) —
    # laissé en commentaire pour reprise future plutôt que supprimé.
    # st.markdown(f"""
    #     <div class="sg-kpi">
    #         <div class="sg-kpi-label">Indice de tension du profil</div>
    #         <div class="sg-kpi-value">{tension_pct}%</div>
    #         <div class="sg-kpi-sub">{_tension_label(tension_pct)}</div>
    #     </div>
    # """, unsafe_allow_html=True)
    # st.markdown('</div>', unsafe_allow_html=True)

    # KPI "Distance technologique" désactivé pour l'instant (voir demande) —
    # laissé en commentaire pour reprise future plutôt que supprimé.
    # st.markdown('<div class="sg-kpi-row">', unsafe_allow_html=True)
    # st.markdown(f"""
    #     <div class="sg-kpi">
    #         <div class="sg-kpi-label">Distance technologique</div>
    #         <div class="sg-kpi-value">{market_fit['avg_similarity']:.2f}</div>
    #         <div class="sg-kpi-sub">similarité moyenne CV / marché (1 = alignement parfait)</div>
    #     </div>
    # """, unsafe_allow_html=True)
    # st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sg-section-title">Offres les plus proches de votre profil</div>', unsafe_allow_html=True)
    for offre in offers[:5]:
        render_offer_card(offre)

    if st.button("Voir toutes les offres →", key="go_to_offres"):
        st.session_state.page = "offres"
        st.rerun()