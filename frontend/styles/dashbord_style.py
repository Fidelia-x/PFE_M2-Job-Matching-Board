import streamlit as st

def inject_dashboard_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap');

    :root {
        --ink-950: #0D1117;
        --ink-900: #151B23;
        --ink-800: #1C232C;
        --ink-700: #262F3B;
        --text-hi: #E8ECF1;
        --text-lo: #8891A0;
        --accent: #3FD6A3;
        --accent-dim: rgba(63, 214, 163, 0.12);
        --amber: #F2B84B;
    }

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

    /* Boutons de nav actifs (Dashboard / Matching) */
    [data-testid="stSidebar"] .stButton button {
        background: transparent;
        border: 1px solid transparent;
        color: var(--text-lo);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        text-align: left;
        justify-content: flex-start;
        padding: 0.55rem 0.9rem;
        border-radius: 8px;
        box-shadow: none;
        transition: background 0.15s ease, color 0.15s ease;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: var(--ink-800);
        color: var(--text-hi);
        border-color: var(--ink-700);
    }
    .st-key-nav_dashboard button {
        background: var(--accent-dim) !important;
        color: var(--accent) !important;
        border-left: 2px solid var(--accent) !important;
        border-radius: 8px !important;
    }

    /* Liens désactivés ("bientôt") */
    .sg-nav-disabled {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.55rem 0.9rem;
        margin: 2px 0;
        color: #545E6B;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    .sg-nav-badge {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #545E6B;
        border: 1px solid var(--ink-700);
        padding: 1px 6px;
        border-radius: 20px;
    }

    .sg-sidebar-footer {
        margin-top: auto;
        padding: 1rem;
        border-top: 1px solid var(--ink-700);
    }

    /* Header de la page */
    .sg-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.4rem 0 1.6rem 0;
        border-bottom: 1px solid var(--ink-700);
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
        box-shadow: 0 0 0 0 rgba(63, 214, 163, 0.5);
        animation: sg-breathe 2.2s ease-in-out infinite;
    }
    @keyframes sg-breathe {
        0%   { box-shadow: 0 0 0 0 rgba(63, 214, 163, 0.45); }
        70%  { box-shadow: 0 0 0 14px rgba(63, 214, 163, 0); }
        100% { box-shadow: 0 0 0 0 rgba(63, 214, 163, 0); }
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
    }
    </style>
    """, unsafe_allow_html=True)