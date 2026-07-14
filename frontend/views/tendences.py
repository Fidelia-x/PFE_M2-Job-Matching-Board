import pandas as pd
import streamlit as st
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header
from views.mock_data import (
    MOCK_TOP_SKILLS, MOCK_CONTRACT_TYPES, MOCK_POSTINGS_OVER_TIME,
    MOCK_SALARY_RANGES, MOCK_CITY_DEMAND,
)


def render_tendences():
    inject_dashboard_style()
    render_sidebar(active_page="tendences")
    render_header(subtitle="Voici les tendances du marché du travail, les demandes, contrats et salaires pour le métier de Data Analyst", title="Tendances du marché")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sg-section-title">Compétences les plus demandées</div>', unsafe_allow_html=True)
        st.bar_chart(pd.Series(MOCK_TOP_SKILLS, name="Offres"))
    with col2:
        st.markdown('<div class="sg-section-title">Types de contrats les plus demandés</div>', unsafe_allow_html=True)
        st.bar_chart(pd.Series(MOCK_CONTRACT_TYPES, name="Offres"))

    st.markdown('<div class="sg-section-title">Offres publiées dans le temps (6 mois)</div>', unsafe_allow_html=True)
    st.bar_chart(pd.Series(MOCK_POSTINGS_OVER_TIME, name="Offres publiées"))

    st.markdown('<div class="sg-section-title">Fourchettes salariales par métier</div>', unsafe_allow_html=True)
    max_salary = max(r["max"] for r in MOCK_SALARY_RANGES)
    for r in MOCK_SALARY_RANGES:
        left_pct = 100 * r["min"] / max_salary
        width_pct = 100 * (r["max"] - r["min"]) / max_salary
        st.markdown(f"""
        <div class="sg-range-row">
            <div class="sg-range-label">{r['metier']}</div>
            <div class="sg-range-track">
                <div class="sg-range-fill" style="left:{left_pct:.1f}%;width:{width_pct:.1f}%"></div>
            </div>
            <div class="sg-range-value">{r['min']}k€ – {r['max']}k€</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sg-section-title">Demande par ville</div>', unsafe_allow_html=True)
    cards = "".join(f"""
        <div class="sg-city-card">
            <div class="sg-city-name">{c['ville']}</div>
            <div class="sg-city-row"><span>Offres</span><span>{c['offres']}</span></div>
            <div class="sg-city-row"><span>Salaire moyen</span><span>{c['salaire_moyen']}</span></div>
            <div class="sg-city-skills">{''.join(f'<span class="sg-city-skill-tag">{s}</span>' for s in c['skills'])}</div>
        </div>
    """ for c in MOCK_CITY_DEMAND)
    st.markdown(f'<div class="sg-city-grid">{cards}</div>', unsafe_allow_html=True)
