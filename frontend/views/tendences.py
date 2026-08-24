import textwrap

import altair as alt
import pandas as pd
import streamlit as st
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header
from back_service.market_stats import get_market_trends, current_month_label, get_active_offers_this_week

# Palette catégorielle (identité) : 8 teintes à ordre fixe, sûres en vision
# des couleurs (voir skill dataviz / references/palette.md). Slots 1..N
# assignés dans l'ordre, jamais recyclés au-delà.
_CATEGORICAL_LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
_CATEGORICAL_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]


@st.cache_data(ttl=600)
def _load_market_trends():
    return get_market_trends()


def _theme_tokens():
    dark = st.session_state.get("dark_mode", False)
    return {
        "dark": dark,
        "colors": _CATEGORICAL_DARK if dark else _CATEGORICAL_LIGHT,
        "accent": "#C97D5D" if dark else "#B5654A",
        "accent_soft": "#5A3F35" if dark else "#E8C9BC",
        "ink": "#F3ECE2" if dark else "#2B2620",
        "muted": "#9C8E7A" if dark else "#8A7F6E",
        "card": "#2A241D" if dark else "#FFFFFF",
        "grid": "#3D352A" if dark else "#ECE3D6",
    }


def _skills_bar_chart(top_skills):
    t = _theme_tokens()
    skills = list(top_skills.keys())
    df = pd.DataFrame({"competence": skills, "offres": list(top_skills.values())})
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, size=28)
        .encode(
            x=alt.X("competence:N", sort="-y", title=None,
                    axis=alt.Axis(labelAngle=-30, labelColor=t["muted"], domainColor=t["grid"], tickColor=t["grid"])),
            y=alt.Y("offres:Q", title="Offres",
                    axis=alt.Axis(labelColor=t["muted"], titleColor=t["muted"], gridColor=t["grid"])),
            color=alt.Color("competence:N",
                             scale=alt.Scale(domain=skills, range=t["colors"][:len(skills)]),
                             legend=None),
            tooltip=[alt.Tooltip("competence:N", title="Compétence"), alt.Tooltip("offres:Q", title="Offres")],
        )
        .properties(height=320, background="transparent")
        .configure_view(strokeWidth=0)
    )
    return chart


def _contract_pie_chart(contract_types):
    t = _theme_tokens()
    contracts = list(contract_types.keys())
    df = pd.DataFrame({"contrat": contracts, "offres": list(contract_types.values())})
    df["pct"] = (df["offres"] / df["offres"].sum() * 100).round(1)
    df["pct_label"] = df["pct"].round(0).astype(int).astype(str) + "%"

    base = alt.Chart(df).encode(
        theta=alt.Theta("offres:Q", stack=True),
        order=alt.Order("offres:Q", sort="descending"),
        color=alt.Color("contrat:N",
                         scale=alt.Scale(domain=contracts, range=t["colors"][:len(contracts)]),
                         legend=alt.Legend(title=None, labelColor=t["ink"], symbolType="circle")),
        tooltip=[alt.Tooltip("contrat:N", title="Contrat"), alt.Tooltip("offres:Q", title="Offres"),
                 alt.Tooltip("pct:Q", title="Part", format=".1f")],
    )
    arc = base.mark_arc(innerRadius=60, stroke=t["card"], strokeWidth=2)
    # Deux lignes empilées via dy (pas de lineBreak natif sur Vega-Lite 4) :
    # le % en gras au-dessus, le type de contrat en dessous, à la même
    # position radiale que la part qu'ils décrivent. `color=alt.value(...)`
    # est indispensable : `base` encode déjà `color` sur `contrat` (pour les
    # parts), donc sans l'écraser ici via un encoding explicite, le texte
    # hérite de cette couleur catégorielle au lieu du `color` passé en
    # propriété du mark — et se retrouve donc de la même teinte que la part
    # sur laquelle il est posé, invisible.
    pct_text = base.mark_text(radius=115, dy=-6, size=12, fontWeight="bold").encode(
        text="pct_label:N", color=alt.value(t["ink"])
    )
    type_text = base.mark_text(radius=115, dy=8, size=9).encode(
        text="contrat:N", color=alt.value(t["ink"])
    )
    return (arc + pct_text + type_text).properties(height=320, background="transparent").configure_view(strokeWidth=0)


def _postings_chart(postings_over_time):
    """Courbe (aire + ligne) plutôt que barres : une série temporelle unique où
    la tendance compte plus que la comparaison entre mois isolés (voir skill
    dataviz, choosing-a-form.md : 'trend over time' -> line/area). L'ordre
    chronologique est fixé explicitement via `sort=months` — un axe nominal
    trierait sinon alphabétiquement ('Avr, Août, Déc, Fév...') plutôt que de
    respecter l'ordre d'insertion du dict, déjà chronologique (voir
    _postings_over_time dans market_stats.py). labelOverlap masque les
    libellés qui se chevauchent quand l'historique compte beaucoup de mois."""
    t = _theme_tokens()
    months = list(postings_over_time.keys())
    df = pd.DataFrame({"mois": months, "offres": list(postings_over_time.values())})
    # Le mois en cours n'est jamais complet (on peut être n'importe quel jour
    # du mois) : son décompte est mécaniquement plus bas que les mois clos et
    # donnerait l'impression trompeuse d'une chute des publications. On le
    # distingue visuellement (marqueur creux + étiquette) plutôt que de le
    # laisser se fondre dans la tendance comme un mois terminé.
    df["is_current"] = df["mois"] == current_month_label()

    x = alt.X("mois:N", sort=months, title=None,
               axis=alt.Axis(labelAngle=-40, labelColor=t["muted"], domainColor=t["grid"],
                              tickColor=t["grid"], labelOverlap=True))
    y = alt.Y("offres:Q", title="Offres publiées",
              axis=alt.Axis(labelColor=t["muted"], titleColor=t["muted"], gridColor=t["grid"]))
    tooltip = [alt.Tooltip("mois:N", title="Mois"), alt.Tooltip("offres:Q", title="Offres")]

    base = alt.Chart(df).encode(x=x, y=y)
    area = base.mark_area(color=t["accent"], opacity=0.15, interpolate="monotone")
    line = base.mark_line(color=t["accent"], strokeWidth=2, interpolate="monotone")
    points_done = base.transform_filter(alt.datum.is_current == False).mark_point(
        color=t["accent"], filled=True, size=50
    ).encode(tooltip=tooltip)
    point_current = base.transform_filter(alt.datum.is_current == True).mark_point(
        color=t["accent"], filled=False, strokeWidth=2, size=90
    ).encode(tooltip=tooltip)
    label_current = base.transform_filter(alt.datum.is_current == True).mark_text(
        dy=-16, size=10, color=t["muted"], fontStyle="italic"
    ).encode(text=alt.value("mois en cours"))

    return (
        (area + line + points_done + point_current + label_current)
        .properties(height=280, background="transparent")
        .configure_view(strokeWidth=0)
    )


def _magnitude_bar_chart(data, label_title, height=280, label_limit=100, gradient=False):
    """Barres horizontales, une seule teinte (accent) : ici la couleur
    n'encode pas une identité (chaque ville n'est pas une 'série') mais une
    magnitude — un seul hue, pas un hue par barre (voir skill dataviz,
    color-formula.md : 'never color nominal bars by their value'). `gradient`
    permet une rampe séquentielle (clair -> accent) sur ce même hue plutôt
    qu'une teinte plate, toujours conforme à la règle ci-dessus puisque la
    couleur encode la magnitude elle-même, pas une identité. `label_limit`
    relève la troncature par défaut de Vega-Lite (100px) : les libellés
    longs (ex. secteurs d'activité) étaient coupés avec '…'."""
    t = _theme_tokens()
    df = pd.DataFrame({"label": list(data.keys()), "offres": list(data.values())})
    df = df.sort_values("offres", ascending=False)
    order = df["label"].tolist()
    color = (
        alt.Color("offres:Q", scale=alt.Scale(range=[t["accent_soft"], t["accent"]]), legend=None)
        if gradient else alt.value(t["accent"])
    )
    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, size=18)
        .encode(
            y=alt.Y("label:N", sort=order, title=None,
                    axis=alt.Axis(labelColor=t["muted"], domainColor=t["grid"], tickColor=t["grid"],
                                   labelLimit=label_limit)),
            x=alt.X("offres:Q", title="Offres",
                    axis=alt.Axis(labelColor=t["muted"], titleColor=t["muted"], gridColor=t["grid"])),
            color=color,
            tooltip=[alt.Tooltip("label:N", title=label_title), alt.Tooltip("offres:Q", title="Offres")],
        )
        .properties(height=height, background="transparent")
        .configure_view(strokeWidth=0)
    )
    return chart


def _city_contract_chart(distribution):
    """Barres empilées horizontales : la ville est la catégorie comparée, le
    type de contrat est l'identité à l'intérieur de chaque barre — donc
    palette catégorielle (une teinte par contrat), pas la teinte unique des
    graphiques de magnitude ci-dessus."""
    t = _theme_tokens()
    df = pd.DataFrame(distribution)
    villes_order = df.groupby("ville")["offres"].sum().sort_values(ascending=False).index.tolist()
    contrats_order = df.groupby("contrat")["offres"].sum().sort_values(ascending=False).index.tolist()

    chart = (
        alt.Chart(df)
        .mark_bar(stroke=t["card"], strokeWidth=1)
        .encode(
            y=alt.Y("ville:N", sort=villes_order, title=None,
                    axis=alt.Axis(labelColor=t["muted"], domainColor=t["grid"], tickColor=t["grid"])),
            x=alt.X("offres:Q", title="Offres", stack="zero",
                    axis=alt.Axis(labelColor=t["muted"], titleColor=t["muted"], gridColor=t["grid"])),
            order=alt.Order("offres:Q", sort="descending"),
            color=alt.Color("contrat:N",
                             scale=alt.Scale(domain=contrats_order, range=t["colors"][:len(contrats_order)]),
                             legend=alt.Legend(title=None, labelColor=t["ink"], orient="bottom", symbolType="square")),
            tooltip=[alt.Tooltip("ville:N", title="Ville"), alt.Tooltip("contrat:N", title="Contrat"),
                     alt.Tooltip("offres:Q", title="Offres")],
        )
        .properties(height=320, background="transparent")
        .configure_view(strokeWidth=0)
    )
    return chart


def render_tendences():
    inject_dashboard_style()
    render_sidebar(active_page="tendences")
    render_header(subtitle="Voici les tendances du marché du travail, les demandes, contrats et salaires pour le métier de Data Analyst", title="Tendances du marché")

    trends = _load_market_trends()

    st.markdown('<div class="sg-kpi-row">', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="sg-kpi">
            <div class="sg-kpi-label">Offres actives cette semaine</div>
            <div class="sg-kpi-value">{get_active_offers_this_week()}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sg-section-title">Compétences les plus demandées</div>', unsafe_allow_html=True)
        if trends["top_skills"]:
            st.altair_chart(_skills_bar_chart(trends["top_skills"]), use_container_width=True)
        else:
            st.info("Pas encore assez de données.")
    with col2:
        st.markdown('<div class="sg-section-title">Types de contrats les plus demandés</div>', unsafe_allow_html=True)
        if trends["contract_types"]:
            st.altair_chart(_contract_pie_chart(trends["contract_types"]), use_container_width=True)
        else:
            st.info("Pas encore assez de données.")

    st.markdown('<div class="sg-section-title">Offres publiées dans le temps</div>', unsafe_allow_html=True)
    if trends["postings_over_time"]:
        st.altair_chart(_postings_chart(trends["postings_over_time"]), use_container_width=True)
    else:
        st.info("Pas encore assez de données.")

    st.markdown('<div class="sg-section-title">Fourchettes salariales par métier</div>', unsafe_allow_html=True)
    salary_ranges = trends["salary_ranges"]
    if not salary_ranges:
        st.info("Pas encore assez de données.")
    else:
        max_salary = max(r["max"] for r in salary_ranges)
        for r in salary_ranges:
            left_pct = 100 * r["min"] / max_salary
            width_pct = 100 * (r["max"] - r["min"]) / max_salary
            # dedent() est indispensable : sans lui, l'indentation Python (12
            # espaces) fait passer le HTML pour un bloc de code Markdown (4+
            # espaces d'indentation), rendu comme texte brut au lieu d'être
            # interprété.
            st.markdown(textwrap.dedent(f"""
                <div class="sg-range-row">
                    <div class="sg-range-label">{r['metier']}</div>
                    <div class="sg-range-track">
                        <div class="sg-range-fill" style="left:{left_pct:.1f}%;width:{width_pct:.1f}%"></div>
                    </div>
                    <div class="sg-range-value">{r['min']}k€ – {r['max']}k€</div>
                </div>
            """), unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="sg-section-title">Demande par ville</div>', unsafe_allow_html=True)
        if trends["city_demand"]:
            st.altair_chart(_magnitude_bar_chart(trends["city_demand"], "Ville"), use_container_width=True)
        else:
            st.info("Pas encore assez de données.")
    with col4:
        st.markdown('<div class="sg-section-title">Distribution des régions</div>', unsafe_allow_html=True)
        if trends["region_demand"]:
            st.altair_chart(_magnitude_bar_chart(trends["region_demand"], "Région"), use_container_width=True)
        else:
            st.info("Pas encore assez de données.")

    st.markdown('<div class="sg-section-title">Types de contrats par ville</div>', unsafe_allow_html=True)
    if trends["city_contract_distribution"]:
        st.altair_chart(_city_contract_chart(trends["city_contract_distribution"]), use_container_width=True)
    else:
        st.info("Pas encore assez de données.")

    st.markdown('<div class="sg-section-title">Secteurs d\'activité qui recrutent le plus</div>', unsafe_allow_html=True)
    if trends["sector_distribution"]:
        st.altair_chart(
            _magnitude_bar_chart(trends["sector_distribution"], "Secteur", height=340, label_limit=260, gradient=True),
            use_container_width=True,
        )
    else:
        st.info("Pas encore assez de données.")
