"""Session state management utilities."""

import streamlit as st
from typing import Any, Optional


def get_session_value(key: str, default: Any = None) -> Any:
    """
    Safely get a value from session state.
    
    Args:
        key: Session state key
        default: Default value if key doesn't exist
    
    Returns:
        Session state value or default
    """
    return st.session_state.get(key, default)


def set_session_value(key: str, value: Any) -> None:
    """
    Set a value in session state.
    
    Args:
        key: Session state key
        value: Value to set
    """
    st.session_state[key] = value


def clear_session_key(key: str) -> None:
    """
    Remove a key from session state.
    
    Args:
        key: Session state key to remove
    """
    if key in st.session_state:
        del st.session_state[key]


def reset_chat_history() -> None:
    """Clear all chat messages from session state."""
    st.session_state.messages = []


def reset_document_state() -> None:
    """Reset document-related session state to defaults."""
    st.session_state.active_doc_name = "Default HR Policy"
    st.session_state.is_custom_doc = False
    st.session_state.active_chunk_count = None
    st.session_state.last_uploaded_name = None


def get_document_info() -> dict:
    """
    Get current document information.
    
    Returns:
        Dictionary with document metadata
    """
    return {
        "name": st.session_state.get("active_doc_name", "Unknown"),
        "is_custom": st.session_state.get("is_custom_doc", False),
        "chunks": st.session_state.get("active_chunk_count", 0),
    }


def get_chat_stats() -> dict:
    """
    Get chat statistics.
    
    Returns:
        Dictionary with chat statistics
    """
    messages = st.session_state.get("messages", [])
    user_messages = [m for m in messages if m["role"] == "user"]
    assistant_messages = [m for m in messages if m["role"] == "assistant"]
    
    return {
        "total": len(messages),
        "user": len(user_messages),
        "assistant": len(assistant_messages),
    }
