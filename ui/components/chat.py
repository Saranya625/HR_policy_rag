"""Chat interface components."""

import re
import streamlit as st

from typing import List, Dict, Optional, Iterable


# ============================================================
# CHAT UI STYLES
# ============================================================

def _inject_chat_styles():
    """Inject styles for the assistant chat UI."""

    st.markdown(
        """
<style>

.assistant-welcome {
    text-align: center;
    padding: 42px 20px 26px 20px;
}

.assistant-welcome-title {
    font-size: 30px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 8px;
}

.assistant-welcome-subtitle {
    font-size: 15px;
    color: var(--text-secondary);
}


/* Suggested prompt buttons */

div[data-testid="column"] button {
    border-radius: 14px !important;
    min-height: 48px !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    color: var(--text) !important;
    transition: all 0.15s ease;
}

div[data-testid="column"] button:hover {
    border-color: var(--primary) !important;
    background: var(--surface-hover) !important;
}


/* Chat messages */

[data-testid="stChatMessage"] {
    padding: 8px 0;
}


/* Chat input */

[data-testid="stChatInput"] {
    padding-bottom: 18px;
}

[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 18px !important;
    font-size: 15px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-secondary) !important;
    opacity: 1 !important;
}


/* Input container */

[data-testid="stChatInput"] > div {
    border-radius: 18px !important;
}


/* Clear chat button */

.clear-chat-wrapper {
    margin-top: 18px;
}

</style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# WELCOME
# ============================================================

def render_welcome():
    """Render assistant welcome section."""

    st.markdown(
        """
<div class="assistant-welcome">
    <div class="assistant-welcome-title">
        How can I help you today?
    </div>

    <div class="assistant-welcome-subtitle">
        Ask anything about your HR policies
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SUGGESTED PROMPTS
# ============================================================

def render_suggested_prompts(
    prompts: List[str],
) -> Optional[str]:
    """
    Render suggested prompt buttons.

    Returns:
        Selected prompt text or None.
    """

    _inject_chat_styles()

    render_welcome()

    selected_prompt = None

    cols_per_row = 2

    for i in range(0, len(prompts), cols_per_row):

        row_prompts = prompts[
            i:i + cols_per_row
        ]

        cols = st.columns(
            len(row_prompts),
            gap="medium",
        )

        for col, prompt in zip(
            cols,
            row_prompts,
        ):

            with col:

                if st.button(
                    prompt,
                    key=f"prompt_{i}_{hash(prompt)}",
                    use_container_width=True,
                ):
                    selected_prompt = prompt

    return selected_prompt


# ============================================================
# SINGLE MESSAGE
# ============================================================

def render_chat_message(
    role: str,
    content: str,
):
    """Render one chat message."""

    with st.chat_message(role):

        st.markdown(content)


# ============================================================
# CONVERSATION
# ============================================================

def render_conversation(
    messages: List[Dict[str, str]],
):
    """Render complete conversation history."""

    for message in messages:

        render_chat_message(
            message["role"],
            message["content"],
        )


# ============================================================
# STREAM
# ============================================================

def render_stream(
    stream: Iterable[str],
) -> str:
    """
    Render a streaming response.

    Returns:
        Complete generated response.
    """

    return st.write_stream(stream)