import streamlit as st
from styles.dashbord_style import inject_dashboard_style
from views.sidebar import render_sidebar
from views.header_board import render_header
from scripts.matching_cv import get_profile_summary
from back_service.chat_service import stream_chat_reply

SUGGESTED_QUESTIONS = [
    "Pourquoi mon score est-il limité ?",
    "Par quoi commencer ?",
    "Quelles offres viser maintenant ?",
    "Comment améliorer mon CV ?",
]


def _profile_context():
    if not st.session_state.get("matching_done"):
        return None
    summary = get_profile_summary(st.session_state.matched_offers)
    if not summary:
        return None
    return summary


def _greeting_message(context):
    prenom = st.session_state.get("user_prenom") or ""
    salutation = f"Bonjour {prenom}." if prenom else "Bonjour."

    if context is None:
        return (
            f"{salutation} Posez-moi vos questions sur votre carrière, vos compétences ou le marché de "
            "l'emploi — ou lancez d'abord un matching CV pour un accompagnement basé sur votre profil."
        )

    skills = context["missing_skills"]
    skills_txt = f" Les compétences à travailler en priorité : {', '.join(skills[:2])}." if skills else ""

    return (
        f"{salutation} J'ai analysé votre CV face au marché : votre correspondance globale est de "
        f"{context['score']}%.{skills_txt} Que voulez-vous approfondir ?"
    )


def _send(question, context):
    st.session_state.chat_messages.append({"role": "user", "content": question})
    with st.spinner("L'assistant réfléchit..."):
        reply_stream = stream_chat_reply(st.session_state.chat_messages, profile_context=context)
        reply = "".join(reply_stream) if reply_stream is not None else (
            "Désolé, l'assistant n'est pas joignable pour le moment (configuration manquante ou service indisponible)."
        )
    st.session_state.chat_messages.append({"role": "assistant", "content": reply})


def render_assistant_ia():
    inject_dashboard_style()
    render_sidebar(active_page="Assistant IA")
    render_header(subtitle="Pose tes questions sur ton profil, tes compétences ou le marché de l'emploi", title="Assistant IA")

    context = _profile_context()

    if not st.session_state.get("chat_messages"):
        st.session_state.chat_messages = [{"role": "assistant", "content": _greeting_message(context)}]

    col_chat, col_context = st.columns([2, 1])

    with col_chat:
        with st.container(border=True):
            st.markdown("""
            <div class="sg-chat-header-row">
                <div class="sg-chat-icon">&#10022;</div>
                <div>
                    <div class="sg-chat-title">Assistant SkillGap</div>
                    <div class="sg-chat-sub">Basé sur votre CV et le marché de l'emploi</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            for i, message in enumerate(st.session_state.chat_messages):
                key_prefix = "bubble_user" if message["role"] == "user" else "bubble_bot"
                with st.container(key=f"{key_prefix}_{i}"):
                    st.markdown(message["content"])

            # Puces de démarrage rapide : seulement tant que la conversation
            # n'a pas commencé (sinon elles encombrent un fil déjà avancé).
            if len(st.session_state.chat_messages) <= 1:
                chip_cols = st.columns(2)
                for i, suggestion in enumerate(SUGGESTED_QUESTIONS):
                    with chip_cols[i % 2]:
                        if st.button(suggestion, key=f"chat_chip_{i}", use_container_width=True):
                            _send(suggestion, context)
                            st.rerun()

            with st.form(key="chat_form", clear_on_submit=True):
                col_input, col_send = st.columns([5, 1])
                with col_input:
                    question = st.text_input(
                        "Question", placeholder="Posez une question sur votre profil...",
                        label_visibility="collapsed",
                    )
                with col_send:
                    submitted = st.form_submit_button("Envoyer", use_container_width=True)

            if submitted and question.strip():
                _send(question.strip(), context)
                st.rerun()

    with col_context:
        with st.container(border=True):
            filename = st.session_state.get("cv_filename") or "—"
            poste_cible = st.session_state.get("cv_target_role") or "Non précisé"
            if context is None:
                st.markdown(f"""
                <div class="sg-context-title">Contexte utilisé</div>
                <div class="sg-context-row"><span class="sg-context-label">CV analysé</span><span class="sg-context-value">—</span></div>
                <div class="sg-context-row"><span class="sg-context-label">Poste cible</span><span class="sg-context-value">—</span></div>
                <div class="sg-context-row"><span class="sg-context-label">Correspondance</span><span class="sg-context-value">—</span></div>
                <div class="sg-context-row"><span class="sg-context-label">Offres compatibles</span><span class="sg-context-value">—</span></div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="sg-context-title">Contexte utilisé</div>
                <div class="sg-context-row"><span class="sg-context-label">CV analysé</span><span class="sg-context-value">{filename}</span></div>
                <div class="sg-context-row"><span class="sg-context-label">Poste cible</span><span class="sg-context-value">{poste_cible}</span></div>
                <div class="sg-context-row"><span class="sg-context-label">Correspondance</span><span class="sg-context-value">{context['score']}%</span></div>
                <div class="sg-context-row"><span class="sg-context-label">Offres compatibles</span><span class="sg-context-value">{context['compatible_count']}</span></div>
                """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("""
            <div class="sg-context-title">Ce que l'assistant peut faire</div>
            <div class="sg-capabilities-text">
                Expliquer un écart de compétence, prioriser vos apprentissages, comparer une offre à
                votre profil, ou répondre à vos questions sur le marché de l'emploi.
            </div>
            """, unsafe_allow_html=True)

        if st.button("Nouvelle conversation", key="chat_reset", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
