"""Navigation bar component."""

import streamlit as st
from typing import List, Tuple


def render_navbar(pages: List[Tuple[str, str]], active_page: str):
    """
    Render a modern navigation bar.
    
    Args:
        pages: List of (label, value) tuples for navigation items
        active_page: Currently active page value
    
    Returns:
        Selected page value
    """
    st.markdown(
        """
        <div style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 0;
            margin-bottom: 32px;
        ">
            <div style="
                font-size: 20px;
                font-weight: 700;
                color: var(--text);
            ">
                HR Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Create pill-style navigation
    cols = st.columns(len(pages))
    selected = active_page
    
    for idx, (col, (label, value)) in enumerate(zip(cols, pages)):
        with col:
            if value == active_page:
                st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            else:
                st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            
            if st.button(label, key=f"nav_{value}", use_container_width=True):
                selected = value
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    return selected
