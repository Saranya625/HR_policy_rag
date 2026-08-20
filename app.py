"""HR Intelligence - Main Application Entry Point"""

import streamlit as st
from src.pipeline import build_hr_assistant

# Import UI components
from ui.components.layout import load_css
from ui.components.navbar import render_navbar
from ui.pages.landing import render_landing_page
from ui.pages.overview import render_overview_page
from ui.pages.documents import render_documents_page
from ui.pages.assistant import render_assistant_page


# Page Configuration
st.set_page_config(
    page_title="HR Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load custom CSS
load_css()


# Initialize session state
def initialize_session_state():
    """Initialize all session state variables."""
    
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_page = "landing"
        st.session_state.agent = None
        st.session_state.messages = []
        st.session_state.active_doc_name = "Default HR Policy"
        st.session_state.is_custom_doc = False
        st.session_state.active_chunk_count = None
        st.session_state.last_uploaded_name = None


initialize_session_state()


# Load agent lazily (cached)
@st.cache_resource(show_spinner=False)
def load_agent():
    """Load the default HR assistant."""
    return build_hr_assistant()


if st.session_state.agent is None and st.session_state.current_page != "landing":
    with st.spinner("Initializing assistant..."):
        st.session_state.agent = load_agent()


# Main Application Router
def main():
    """Main application entry point and router."""
    
    # Landing page - no navigation
    if st.session_state.current_page == "landing":
        get_started = render_landing_page()
        
        if get_started:
            st.session_state.current_page = "overview"
            st.rerun()
    
    # Main application pages - with navigation
    else:
        # Navigation
        pages = [
            ("Overview", "overview"),
            ("Documents", "documents"),
            ("Assistant", "assistant"),
        ]
        
        selected_page = render_navbar(pages, st.session_state.current_page)
        
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()
        
        # Render active page
        if st.session_state.current_page == "overview":
            render_overview_page()
        
        elif st.session_state.current_page == "documents":
            render_documents_page()
        
        elif st.session_state.current_page == "assistant":
            render_assistant_page()


if __name__ == "__main__":
    main()
