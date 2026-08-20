"""Overview/Dashboard page."""

import streamlit as st
from ui.components.layout import page_header, section_header, spacer
from ui.components.cards import stat_card, document_card, info_card


def render_overview_page():
    """Render the overview/dashboard page."""
    
    page_header(
        "Overview",
        "Monitor your knowledge base and system status"
    )
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        chunks = st.session_state.get("active_chunk_count", 0)
        stat_card(
            label="Total Chunks",
            value=str(chunks) if chunks else "N/A",
            sublabel="Indexed segments"
        )
    
    with col2:
        messages = len(st.session_state.get("messages", []))
        stat_card(
            label="Conversations",
            value=str(messages),
            sublabel="Messages exchanged"
        )
    
    with col3:
        stat_card(
            label="Status",
            value="Active",
            sublabel="System operational"
        )
    
    with col4:
        doc_type = "Custom" if st.session_state.get("is_custom_doc", False) else "Default"
        stat_card(
            label="Document",
            value=doc_type,
            sublabel="Knowledge source"
        )
    
    spacer("32px")
    
    # Knowledge Base Section
    section_header("Knowledge Base", "Current active document configuration")
    
    doc_name = st.session_state.get("active_doc_name", "Default HR Policy")
    is_custom = st.session_state.get("is_custom_doc", False)
    chunk_count = st.session_state.get("active_chunk_count", 0)
    
    display_name = doc_name if is_custom else "Company HR Policy (Default)"
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        replace, reset = document_card(
            filename=display_name,
            chunks=chunk_count if chunk_count else 0,
            status="Active",
            show_actions=True
        )
        
        if replace:
            st.session_state.current_page = "documents"
            st.rerun()
        
        if reset:
            from src.pipeline import build_hr_assistant
            
            with st.spinner("Resetting to default..."):
                st.session_state.agent = build_hr_assistant()
                st.session_state.active_doc_name = "Default HR Policy"
                st.session_state.is_custom_doc = False
                st.session_state.active_chunk_count = None
                st.session_state.last_uploaded_name = None
                st.session_state.messages = []
            
            st.success("Reset to default HR policy successfully")
            st.rerun()
    
    with col2:
        info_card(
            title="Embedding Model",
            content="sentence-transformers/all-MiniLM-L6-v2",
            status="Active",
            status_type="success"
        )
        
        spacer("16px")
        
        info_card(
            title="Vector Store",
            content="FAISS (Facebook AI Similarity Search)",
            status="Ready",
            status_type="success"
        )
    
    spacer("32px")
    
    # Quick Actions
    section_header("Quick Actions", "Navigate to key features")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Open Assistant", key="quick_assistant", use_container_width=True):
            st.session_state.current_page = "assistant"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("Upload Document", key="quick_upload", use_container_width=True):
            st.session_state.current_page = "documents"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("Clear Chat", key="quick_clear", use_container_width=True):
            st.session_state.messages = []
            st.success("Chat history cleared")
        st.markdown('</div>', unsafe_allow_html=True)
    
    spacer("32px")
    
    # Recent Activity
    if st.session_state.get("messages"):
        section_header("Recent Activity", "Latest conversation messages")
        
        recent_messages = st.session_state.messages[-5:]  # Last 5 messages
        
        for msg in recent_messages:
            role_display = "You" if msg["role"] == "user" else "Assistant"
            preview = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            
            st.markdown(
                f"""
                <div class="card" style="margin-bottom: 8px;">
                    <div style="font-size: 12px; font-weight: 600; color: var(--text-muted); margin-bottom: 4px;">
                        {role_display}
                    </div>
                    <div style="font-size: 14px; color: var(--text-secondary);">
                        {preview}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
