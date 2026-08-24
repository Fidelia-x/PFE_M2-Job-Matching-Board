import streamlit as st
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header
from views.gating import require_matching
from scripts.matching_cv import rank_missing_skills
from scripts.training_catalog import get_trainings_for_skill, search_fallback_link
from back_service.recommendation_service import get_skill_advice

# Nombre d'écarts de compétences traités : au-delà, la page devient trop
# longue et le candidat perd le fil des priorités réelles.
MAX_SKILLS = 5


@st.cache_data(ttl=600, show_spinner=False)
def _cached_skill_advice(skills):
    return get_skill_advice(list(skills))


def render_recommendation():
    inject_dashboard_style()
    render_sidebar(active_page="recommendation")
    render_header(subtitle="Voici les recommandations de formations adaptées à votre profil pour combler vos écarts", title="Recommandations de formations")

    if not require_matching():
        return

    ranked_gaps = rank_missing_skills(st.session_state.matched_offers)[:MAX_SKILLS]
    if not ranked_gaps:
        st.info("Aucun écart de compétence détecté par rapport aux offres analysées pour le moment.")
        return

    advice = _cached_skill_advice(tuple(skill for skill, _ in ranked_gaps))

    for skill, pct in ranked_gaps:
        trainings = get_trainings_for_skill(skill)
        if trainings:
            for formation in trainings:
                lien = formation.get("lien")
                titre = (
                    f'<a href="{lien}" target="_blank" rel="noopener noreferrer">{formation["nom"]} ↗</a>'
                    if lien else formation["nom"]
                )
                st.markdown(f"""
                <div class="sg-training-card">
                    <p class="sg-training-title">{titre}</p>
                    <p class="sg-training-meta">{formation['organisme']} · {formation['duree']} · comble : {skill} (absente de {pct}% des offres)</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Ne devrait plus arriver pour une compétence du référentiel
            # (catalogue couvre les 96), mais reste un filet de sécurité si
            # le référentiel s'agrandit avant que le catalogue suive.
            fallback = search_fallback_link(skill)
            st.markdown(f"""
            <div class="sg-training-card">
                <p class="sg-training-title"><a href="{fallback}" target="_blank" rel="noopener noreferrer">Rechercher des formations "{skill}" ↗</a></p>
                <p class="sg-training-meta">Absente de {pct}% des offres — pas encore de formation référencée précisément pour cette compétence.</p>
            </div>
            """, unsafe_allow_html=True)

        skill_advice = advice.get(skill)
        if skill_advice:
            st.markdown(f"""
            <div class="sg-training-card">
                <p class="sg-training-title">Projet suggéré — {skill}</p>
                <p class="sg-training-meta">{skill_advice.get('projet_suggere', '')}</p>
                <p class="sg-training-meta">{skill_advice.get('conseil', '')}</p>
            </div>
            """, unsafe_allow_html=True)
