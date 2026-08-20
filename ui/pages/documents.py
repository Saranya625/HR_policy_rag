"""Document upload and management page."""

import streamlit as st
from ui.components.layout import page_header, section_header, spacer, centered_container
from ui.components.cards import info_card


def render_documents_page():
    """Render the documents upload page."""
    
    page_header(
        "Documents",
        "Upload and manage your HR policy documents"
    )
    
    # Upload Section
    st.markdown(
        """
        <div style="
            max-width: 700px;
            margin: 0 auto;
            text-align: center;
        ">
            <h2 style="
                font-size: 24px;
                font-weight: 600;
                color: var(--text);
                margin-bottom: 16px;
            ">
                Upload HR Document
            </h2>
            <p style="
                font-size: 15px;
                color: var(--text-secondary);
                margin-bottom: 32px;
                line-height: 1.6;
            ">
                Upload your company's HR policies, handbooks, or guidelines. 
                Supported formats include PDF, Markdown, and plain text files.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # File Uploader
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["txt", "md", "pdf"],
            help="Upload your HR policy document",
            label_visibility="collapsed",
        )
        
        if uploaded_file is not None:
            last_uploaded = st.session_state.get("last_uploaded_name")
            
            if last_uploaded != uploaded_file.name:
                with st.spinner("Processing document..."):
                    try:
                        from src.pipeline import build_hr_assistant_from_upload
                        
                        file_bytes = uploaded_file.getvalue()
                        new_agent, chunk_count = build_hr_assistant_from_upload(
                            file_bytes, uploaded_file.name
                        )
                        
                        # Update session state
                        st.session_state.agent = new_agent
                        st.session_state.active_doc_name = uploaded_file.name
                        st.session_state.is_custom_doc = True
                        st.session_state.active_chunk_count = chunk_count
                        st.session_state.last_uploaded_name = uploaded_file.name
                        st.session_state.messages = []
                        
                        st.success(
                            f"Successfully indexed **{uploaded_file.name}** with {chunk_count} chunks"
                        )
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"Failed to process document: {str(e)}")
            else:
                st.info(f"**{uploaded_file.name}** is already indexed and active")
    
    spacer("48px")
    
    # Current Document Info
    if st.session_state.get("is_custom_doc"):
        section_header("Active Document", "Currently indexed document")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            doc_name = st.session_state.get("active_doc_name", "Unknown")
            chunk_count = st.session_state.get("active_chunk_count", 0)
            
            st.markdown(
                f"""
                <div class="card">
                    <div style="margin-bottom: 16px;">
                        <h3 style="
                            font-size: 18px;
                            font-weight: 600;
                            color: var(--text);
                            margin-bottom: 8px;
                        ">
                            {doc_name}
                        </h3>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <span class="status-pill status-success">Active</span>
                            <span class="status-pill status-info">{chunk_count} chunks</span>
                        </div>
                    </div>
                    <p style="
                        font-size: 13px;
                        color: var(--text-muted);
                        margin-bottom: 16px;
                    ">
                        This document is currently being used as the knowledge base for the assistant.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            spacer("16px")
            
            # Actions
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
                if st.button("View in Assistant", key="view_assistant", use_container_width=True):
                    st.session_state.current_page = "assistant"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_b:
                st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
                if st.button("Reset to Default", key="reset_to_default", use_container_width=True):
                    from src.pipeline import build_hr_assistant
                    
                    with st.spinner("Resetting..."):
                        st.session_state.agent = build_hr_assistant()
                        st.session_state.active_doc_name = "Default HR Policy"
                        st.session_state.is_custom_doc = False
                        st.session_state.active_chunk_count = None
                        st.session_state.last_uploaded_name = None
                        st.session_state.messages = []
                    
                    st.success("Reset to default HR policy")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    
    spacer("48px")
    
    # Instructions
    section_header("Supported Formats", "File types and guidelines")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown(
            """
            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                <div style="font-size: 16px; font-weight: 600; color: #111827; margin-bottom: 12px;">PDF Files</div>
                <div style="font-size: 14px; color: #6B7280; line-height: 1.6;">Standard PDF documents with text content. Images and scanned documents may not work correctly.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                <div style="font-size: 16px; font-weight: 600; color: #111827; margin-bottom: 12px;">Markdown</div>
                <div style="font-size: 14px; color: #6B7280; line-height: 1.6;">Markdown files (.md) with formatted text. Ideal for structured documentation.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                <div style="font-size: 16px; font-weight: 600; color: #111827; margin-bottom: 12px;">Plain Text</div>
                <div style="font-size: 14px; color: #6B7280; line-height: 1.6;">Simple text files (.txt) containing policy information and guidelines.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    spacer("32px")
    
    # Tips
    st.markdown(
        """
        <div class="card" style="background: var(--primary-light); border-color: var(--primary);">
            <h3 style="
                font-size: 16px;
                font-weight: 600;
                color: var(--text);
                margin-bottom: 12px;
            ">
                Tips for Best Results
            </h3>
            <ul style="
                font-size: 14px;
                color: var(--text-secondary);
                line-height: 1.8;
                margin-left: 20px;
            ">
                <li>Use well-structured documents with clear headings</li>
                <li>Ensure text is searchable (not scanned images)</li>
                <li>Include comprehensive policy information</li>
                <li>Keep documents focused on HR-related content</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
