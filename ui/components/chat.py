"""Chat interface components."""

import streamlit as st

from typing import List, Dict, Optional, Iterable


# ============================================================
# CHAT UI STYLES
# ============================================================

def _inject_chat_styles():
    """Inject styles specific to the assistant page."""

    st.markdown(
        """
<style>

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

[data-testid="stChatMessage"] {
    padding: 8px 0;
}

[data-testid="stChatInput"] {
    padding-bottom: 18px;
}

[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    background: var(--surface) !important;
    font-size: 15px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-secondary) !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] > div {
    border-radius: 18px !important;
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

    st.html(
        """
        <div style="
            text-align: center;
            padding: 32px 20px 24px 20px;
        ">
            <div style="
                font-size: 30px;
                font-weight: 700;
                color: var(--text);
                margin-bottom: 8px;
            ">
                How can I help you today?
            </div>

            <div style="
                font-size: 15px;
                color: var(--text-secondary);
            ">
                Ask anything about your HR policies
            </div>
        </div>
        """
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

    for i in range(0, len(prompts), 2):

        row_prompts = prompts[i:i + 2]

        cols = st.columns(
            len(row_prompts),
            gap="medium",
        )

        for col, prompt in zip(
            cols,
            row_prompts,
        ):

            with col:

                # Wrapper used to scope prompt-specific CSS
                st.markdown(
                    '<div class="assistant-prompt">',
                    unsafe_allow_html=True,
                )

                if st.button(
                    prompt,
                    key=f"prompt_{i}_{hash(prompt)}",
                    use_container_width=True,
                ):
                    selected_prompt = prompt

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )

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
    thinking=None,
) -> str:
    """Render streaming response without an empty assistant box."""

    answer = ""
    first_chunk = True
    response_placeholder = None

    for chunk in stream:

        # ----------------------------------------------------
        # FIRST RESPONSE CHUNK
        # ----------------------------------------------------

        if first_chunk:

            first_chunk = False

            # Remove Thinking...
            if thinking is not None:
                thinking.empty()

            # Create assistant message ONLY after
            # the first response chunk arrives
            with st.chat_message("assistant"):
                response_placeholder = st.empty()

        # ----------------------------------------------------
        # ADD CHUNK
        # ----------------------------------------------------

        answer += str(chunk)

        # ----------------------------------------------------
        # UPDATE RESPONSE
        # ----------------------------------------------------

        if response_placeholder is not None:
            response_placeholder.markdown(answer)

    # --------------------------------------------------------
    # NO RESPONSE
    # --------------------------------------------------------

    if first_chunk:

        if thinking is not None:
            thinking.empty()

    return answer