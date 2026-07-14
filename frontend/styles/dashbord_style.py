import streamlit as st

_LIGHT = dict(
    bg="#FAF7F2", bg2="#F3EEE6", card="#FFFFFF", surface="#EAE3D8", border="#ECE3D6",
    text_hi="#2B2620", text_lo="#5B5346", text_discreet="#8A7F6E",
    accent="#B5654A", accent_dim="rgba(181, 101, 74, 0.12)", accent_ink="#FFF8F3",
    amber="#C9A227",
    success="oklch(0.58 0.12 150)", warning="oklch(0.72 0.14 78)", danger="oklch(0.58 0.17 26)",
    success_dim="oklch(0.58 0.12 150 / 0.12)", warning_dim="oklch(0.72 0.14 78 / 0.12)", danger_dim="oklch(0.58 0.17 26 / 0.12)",
)

_DARK = dict(
    bg="#211C17", bg2="#2F281F", card="#2A241D", surface="#332B21", border="#3D352A",
    text_hi="#F3ECE2", text_lo="#CBBFAE", text_discreet="#9C8E7A",
    accent="#C97D5D", accent_dim="rgba(201, 125, 93, 0.18)", accent_ink="#211C17",
    amber="#D9B54A",
    success="oklch(0.68 0.12 150)", warning="oklch(0.78 0.14 78)", danger="oklch(0.68 0.17 26)",
    success_dim="oklch(0.68 0.12 150 / 0.16)", warning_dim="oklch(0.78 0.14 78 / 0.16)", danger_dim="oklch(0.68 0.17 26 / 0.16)",
)

_STATIC_CSS = """
/* Fond général de l'app */
[data-testid="stAppViewContainer"] {
    background: var(--ink-950);
}
[data-testid="stHeader"] {
    background: transparent;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--ink-900);
    border-right: 1px solid var(--ink-700);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}
/* stSidebarContent est le vrai conteneur défilant (height:100%; overflow:auto)
   défini par Streamlit. Son contenu se répartit en [stSidebarHeader, stSidebarUserContent] :
   c'est stSidebarUserContent (pas son premier enfant, qui est le header/logo) qui
   contient les éléments ajoutés via `with st.sidebar:`. On le fait grandir en
   flex:1 jusqu'au bas du conteneur, puis on pousse le profil tout en bas avec
   margin-top:auto sur son propre bloc vertical. */
[data-testid="stSidebarContent"] {
    height: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}
[data-testid="stSidebarUserContent"] {
    flex: 1;
    display: flex;
    flex-direction: column;
}
[data-testid="stSidebarUserContent"] > div:first-child {
    display: flex;
    flex-direction: column;
    flex: 1;
}
/* Le bloc vertical qui contient réellement le logo/les boutons de nav/le
   footer (stVerticalBlock) est UN NIVEAU PLUS BAS que div:first-child (qui
   n'est qu'un wrapper neutre). Streamlit donne nativement flex:1 1 0% à
   stVerticalBlock lui-même (jamais flex:1 1 auto), donc sans override il ne
   grandit pas assez pour remplir tout l'espace disponible : on force flex:1
   dessus, puis on neutralise le flex-grow de tous ses enfants directs (logo,
   boutons, footer) pour que l'espace libre ne soit capté que par le
   margin-top:auto du footer (voir plus bas), au lieu d'être réparti entre
   tous les éléments. */
[data-testid="stSidebarUserContent"] > div:first-child > [data-testid="stVerticalBlock"] {
    flex: 1 1 auto !important;
}
[data-testid="stSidebarUserContent"] > div:first-child > [data-testid="stVerticalBlock"] > * {
    flex: 0 0 auto !important;
}

.sg-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 1rem 1.5rem 1rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--ink-700);
}
.sg-logo-dot {
    width: 10px;
    height: 10px;
    border-radius: 3px;
    background: var(--accent);
    flex-shrink: 0;
}
.sg-logo-text {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--text-hi);
    letter-spacing: -0.01em;
}

.sg-nav-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    color: var(--text-lo);
    text-transform: uppercase;
    padding: 0.5rem 1rem 0.4rem 1rem;
}

/* Boutons de nav (sidebar) */
[data-testid="stSidebar"] .stButton button {
    background: transparent;
    border: 1px solid transparent;
    color: var(--text-lo);
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.55rem 0.9rem;
    border-radius: 8px;
    box-shadow: none;
    transition: background 0.15s ease, color 0.15s ease;
}
[data-testid="stSidebar"] .stButton button p {
    color: inherit;
    width: 100% !important;
    text-align: left !important;
}
[data-testid="stSidebar"] .stButton button div[data-testid="stMarkdownContainer"] {
    width: 100%;
    text-align: left !important;
}
/* Filet de sécurité : force l'alignement sur tout descendant du bouton,
   quelle que soit la balise utilisée par la version de Streamlit */
[data-testid="stSidebar"] .stButton button * {
    text-align: left !important;
    justify-content: flex-start !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: transparent;
    color: var(--text-hi);
    border-color: transparent;
}
/* Le bouton de nav actif est surligné dynamiquement selon active_page (voir sidebar.py) */

/* Badge "bientôt" sur le bouton Assistant IA */
.st-key-nav_assistant button {
    display: flex;
}
.st-key-nav_assistant button::after {
    content: "bientôt";
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--text-lo);
    border: 1px solid var(--ink-700);
    padding: 1px 6px;
    border-radius: 20px;
    margin-left: auto;
    flex-shrink: 0;
}

/* Liens désactivés ("bientôt") */
.sg-nav-disabled {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.55rem 0.9rem;
    margin: 2px 0;
    color: var(--text-discreet);
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
}
.sg-nav-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--text-discreet);
    border: 1px solid var(--ink-700);
    padding: 1px 6px;
    border-radius: 20px;
}

.st-key-sg_sidebar_footer {
    margin-top: auto;
    padding: 1rem;
    border-top: 1px solid var(--ink-700);
}

/* Profil (déclencheur du popover) */
.sg-profile-trigger {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.4rem 0.5rem;
}
.sg-profile-name {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--text-hi);
    line-height: 1.2;
}
.sg-profile-role {
    font-family: 'Inter', sans-serif;
    font-size: 0.76rem;
    color: var(--text-discreet);
}
[data-testid="stSidebar"] [data-testid="stPopoverBody"] {
    background: var(--card-bg);
    border: 1px solid var(--ink-700);
}
.sg-popover-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-discreet);
    margin: 0.2rem 0 0.3rem 0;
}

/* Header de la page */
.sg-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.4rem 0 1.6rem 0;
    border-bottom: 1px solid var(--ink-700);
    margin-bottom: 2.5rem;
    flex-wrap: wrap;
    gap: 1rem;
}
.st-key-sg_header_row {
    border-bottom: 1px solid var(--ink-700);
    padding: 0.4rem 0 1.6rem 0;
    margin-bottom: 2.5rem;
}
.sg-header-greeting {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.6rem;
    color: var(--text-hi);
    margin: 0;
}
.sg-header-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    color: var(--text-lo);
    margin-top: 0.2rem;
}
.sg-header-right {
    display: flex;
    align-items: center;
    gap: 14px;
}
.sg-search {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--text-lo);
    background: var(--ink-800);
    border: 1px solid var(--ink-700);
    border-radius: 8px;
    padding: 0.5rem 0.9rem;
    width: 220px;
}
.sg-bell {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--ink-800);
    border: 1px solid var(--ink-700);
    border-radius: 8px;
    color: var(--text-lo);
    position: relative;
}
.sg-bell::after {
    content: "";
    position: absolute;
    top: 8px;
    right: 8px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--amber);
}
/* Zone placeholder centrale */
.sg-placeholder-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 5rem 1rem;
    min-height: 40vh;
}
.sg-pulse {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--accent);
    margin-bottom: 1.6rem;
    box-shadow: 0 0 0 0 rgba(181, 101, 74, 0.5);
    animation: sg-breathe 2.2s ease-in-out infinite;
}
@keyframes sg-breathe {
    0%   { box-shadow: 0 0 0 0 rgba(181, 101, 74, 0.45); }
    70%  { box-shadow: 0 0 0 14px rgba(181, 101, 74, 0); }
    100% { box-shadow: 0 0 0 0 rgba(181, 101, 74, 0); }
}
@media (prefers-reduced-motion: reduce) {
    .sg-pulse { animation: none; }
}
.sg-placeholder-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.3rem;
    color: var(--text-hi);
    margin: 0 0 0.5rem 0;
}
.sg-placeholder-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    color: var(--text-lo);
    max-width: 380px;
    line-height: 1.5;
}
.sg-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--accent-dim);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    flex-shrink: 0;
}

/* Radar chart & jauge (Matching CV) */
.sg-radar-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.sg-radar-legend {
    display: flex;
    gap: 1.2rem;
    margin-top: 0.75rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    color: var(--text-lo);
}
.sg-radar-legend span {
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.sg-radar-legend i {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 3px;
}
.sg-gauge-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
}

/* Zone de dépôt du CV (étape 1 du Matching) */
.st-key-cv_dropzone {
    border: 2px dashed var(--ink-700);
    border-radius: 16px;
    background: var(--card-bg);
    padding: 2.5rem 2rem 2rem 2rem;
    text-align: center;
    max-width: 620px;
    margin: 0 auto 1.5rem auto;
}
.sg-dropzone-icon {
    font-size: 2.1rem;
    margin-bottom: 0.75rem;
}
.sg-dropzone-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--text-hi);
    margin: 0 0 0.35rem 0;
}
.sg-dropzone-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.86rem;
    color: var(--text-lo);
    margin-bottom: 1.4rem;
}
/* On neutralise le cadre natif du file_uploader Streamlit imbriqué (on a déjà
   notre propre cadre en pointillés autour de tout le dropzone) mais on garde
   son bouton "Browse files" : c'est le seul moyen de choisir un fichier au
   clic (le glisser-déposer seul n'est pas assez visible/découvrable). */
.st-key-cv_dropzone [data-testid="stFileUploaderDropzone"] {
    border: none;
    background: transparent;
    padding: 0;
    justify-content: center;
}
.st-key-cv_dropzone [data-testid="stFileUploaderDropzoneInstructions"] {
    display: none;
}
.st-key-cv_dropzone [data-testid="stFileUploader"] {
    margin-bottom: 1rem;
}
.st-key-cv_dropzone [data-testid="stFileUploader"] button {
    background: var(--accent) !important;
    color: var(--accent-ink) !important;
    border: none !important;
    font-weight: 600 !important;
}
.st-key-cv_dropzone .stButton button {
    background: var(--accent) !important;
    color: var(--accent-ink) !important;
    border: none !important;
    font-weight: 600 !important;
}

/* Cartes génériques */
.sg-card {
    background: var(--card-bg);
    border: 1px solid var(--ink-700);
    border-radius: 12px;
    padding: 1.25rem;
}

/* Grille de KPI (jamais plus de 3 par ligne) */
.sg-kpi-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(0, 1fr));
    grid-auto-flow: column;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.sg-kpi-row > .sg-kpi:nth-child(n+4) { display: none; }
.sg-kpi {
    background: var(--card-bg);
    border: 1px solid var(--ink-700);
    border-radius: 12px;
    padding: 1rem 1.25rem;
}
.sg-kpi-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-discreet);
    margin-bottom: 0.4rem;
}
.sg-kpi-value {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.7rem;
    color: var(--text-hi);
}

/* Pastilles de statut (couleur seule, pas d'icône) */
.sg-pill {
    display: inline-flex;
    align-items: center;
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
}
.sg-pill-success { background: var(--success-dim); color: var(--success); }
.sg-pill-warning { background: var(--warning-dim); color: var(--warning); }
.sg-pill-danger  { background: var(--danger-dim);  color: var(--danger); }

/* Bandeau CTA (ex: vers Recommandations) */
.sg-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    background: var(--accent-dim);
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.sg-banner-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: var(--text-hi);
}
.sg-banner-text strong { color: var(--accent); }

/* Écran de blocage (gating) */
.sg-gate-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4rem 1rem;
    min-height: 40vh;
}
.sg-gate-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.25rem;
    color: var(--text-hi);
    margin: 0 0 0.5rem 0;
}
.sg-gate-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    color: var(--text-lo);
    max-width: 420px;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}
.st-key-go_to_matching button, .st-key-go_to_matching_reco button {
    background: var(--accent) !important;
    color: var(--accent-ink) !important;
    border: 1px solid var(--accent) !important;
}

/* Tableau détaillé de compétences */
.sg-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Inter', sans-serif;
    font-size: 0.86rem;
}
.sg-table th {
    text-align: left;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-discreet);
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--ink-700);
}
.sg-table td {
    padding: 0.6rem 0.75rem;
    border-bottom: 1px solid var(--ink-700);
    color: var(--text-hi);
}

/* Cartes d'offres */
.sg-offer-card {
    background: var(--card-bg);
    border: 1px solid var(--ink-700);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
/* Le sélecteur de Streamlit pour les liens dans le markdown (scopé sur
   stMarkdownContainer) est plus spécifique qu'une simple classe : on doit
   matcher "a.sg-offer-card" (pas juste ".sg-offer-card") et neutraliser tout
   descendant pour que le soulignement ne traverse pas les enfants. */
a.sg-offer-card,
a.sg-offer-card * {
    text-decoration: none !important;
}
a.sg-offer-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
}
.sg-offer-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.02rem;
    color: var(--text-hi);
    margin: 0 0 0.2rem 0;
}
.sg-offer-meta {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: var(--text-lo);
}
.sg-offer-score {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--accent);
    text-align: right;
}
.sg-offer-score-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--text-discreet);
    text-align: right;
}

/* Cartes de formation (Recommandations) */
.sg-training-card {
    background: var(--card-bg);
    border: 1px solid var(--ink-700);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.9rem;
}
.sg-training-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    color: var(--text-hi);
    margin: 0 0 0.3rem 0;
}
.sg-training-meta {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: var(--text-lo);
}

/* Barres de plage salariale */
.sg-range-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}
.sg-range-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: var(--text-hi);
    width: 190px;
    flex-shrink: 0;
}
.sg-range-track {
    position: relative;
    flex: 1;
    height: 8px;
    background: var(--ink-800);
    border-radius: 4px;
}
.sg-range-fill {
    position: absolute;
    top: 0;
    height: 100%;
    background: var(--accent);
    border-radius: 4px;
}
.sg-range-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-discreet);
    width: 130px;
    text-align: right;
    flex-shrink: 0;
}

/* Cartes ville (demande par ville) */
.sg-city-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}
.sg-city-card {
    background: var(--card-bg);
    border: 1px solid var(--ink-700);
    border-radius: 12px;
    padding: 1rem 1.1rem;
}
.sg-city-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.98rem;
    color: var(--text-hi);
    margin-bottom: 0.5rem;
}
.sg-city-row {
    display: flex;
    justify-content: space-between;
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: var(--text-lo);
    padding: 2px 0;
}
.sg-city-skills {
    margin-top: 0.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}
.sg-city-skill-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    color: var(--text-lo);
    background: var(--ink-800);
    border: 1px solid var(--ink-700);
    border-radius: 20px;
    padding: 2px 8px;
}

/* Section title générique */
.sg-section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--text-hi);
    margin: 2rem 0 1rem 0;
}
.sg-section-title:first-child { margin-top: 0; }

/* Guide de conception */
.sg-guide-hero {
    font-family: 'Inter', sans-serif;
    font-size: 0.94rem;
    color: var(--text-lo);
    max-width: 640px;
    line-height: 1.6;
    margin-bottom: 1rem;
}
.sg-guide-tree {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-hi);
    line-height: 2;
}
.sg-guide-tree b { color: var(--accent); }
.sg-swatch-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.9rem;
    margin: 0.75rem 0 1.5rem 0;
}
.sg-swatch {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-lo);
}
.sg-swatch-chip {
    width: 56px;
    height: 56px;
    border-radius: 10px;
    border: 1px solid var(--ink-700);
}
"""


def inject_dashboard_style():
    c = _DARK if st.session_state.get("dark_mode", False) else _LIGHT

    root_vars = f"""
    :root {{
        --ink-950: {c['bg']};
        --ink-900: {c['bg2']};
        --ink-800: {c['surface']};
        --ink-700: {c['border']};
        --card-bg: {c['card']};
        --text-hi: {c['text_hi']};
        --text-lo: {c['text_lo']};
        --text-discreet: {c['text_discreet']};
        --accent: {c['accent']};
        --accent-dim: {c['accent_dim']};
        --accent-ink: {c['accent_ink']};
        --amber: {c['amber']};
        --success: {c['success']};
        --warning: {c['warning']};
        --danger: {c['danger']};
        --success-dim: {c['success_dim']};
        --warning-dim: {c['warning_dim']};
        --danger-dim: {c['danger_dim']};
    }}
    """

    css = (
        "<style>\n"
        "@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap');\n"
        + root_vars
        + _STATIC_CSS
        + "\n</style>"
    )
    st.markdown(css, unsafe_allow_html=True)
