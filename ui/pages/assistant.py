"""AI Assistant chat page."""

import streamlit as st

from ui.components.layout import page_header
from ui.components.chat import (
    render_suggested_prompts,
    render_conversation,
    render_stream,
)

from src.pipeline import (
    ask_stream,
)


def render_assistant_page():
    """Render the AI assistant chat interface."""

    # ========================================================
    # HEADER
    # ========================================================

    page_header(
        "Assistant",
        "Ask questions about your HR policies and get instant answers",
    )

    # ========================================================
    # CHAT STATE
    # ========================================================

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ========================================================
    # WELCOME + SUGGESTIONS
    # ========================================================

    if not st.session_state.messages:

        suggested_prompts = [
            "What is the work from home policy?",
            "How many vacation days do employees get?",
            "What is the notice period for resignation?",
            "Explain the health insurance benefits",
        ]

        selected_prompt = render_suggested_prompts(
            suggested_prompts
        )

        if selected_prompt:

            _process_query(
                selected_prompt
            )

            st.rerun()

    # ========================================================
    # CONVERSATION
    # ========================================================

    if st.session_state.messages:

        render_conversation(
            st.session_state.messages
        )

    # ========================================================
    # CHAT INPUT
    # ========================================================

    user_query = st.chat_input(
        "Ask a question about your HR policies..."
    )

    if user_query:

        _process_query(
            user_query
        )

        st.rerun()

    # ========================================================
    # ACTIONS
    # ========================================================

    if st.session_state.messages:

        st.markdown(
            "<div style='height: 8px'></div>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(
            [1, 1, 1],
            gap="small",
        )

        with col2:

            if st.button(
                "Clear Chat",
                key="clear_chat",
                use_container_width=True,
            ):

                st.session_state.messages = []

                st.rerun()

        with col3:

            if st.button(
                "View Overview",
                key="view_overview",
                use_container_width=True,
            ):

                st.session_state.current_page = (
                    "overview"
                )

                st.rerun()


# ============================================================
# PROCESS QUERY
# ============================================================

def _process_query(
    query: str,
):
    """Process a user query with streaming."""

    # --------------------------------------------------------
    # Save user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    # --------------------------------------------------------
    # User message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(query)

    # --------------------------------------------------------
    # Assistant response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        try:

            answer = render_stream(
                ask_stream(
                    st.session_state.agent,
                    query,
                )
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as e:

            error_message = (
                f"An error occurred: {str(e)}"
            )

            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )