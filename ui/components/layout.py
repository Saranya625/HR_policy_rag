"""Layout utilities and helpers."""

import streamlit as st
from pathlib import Path


def load_css():
    """Load custom CSS styles."""
    css_path = Path(__file__).parent.parent / "styles.css"
    
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS file not found")


def page_header(title: str, subtitle: str = ""):
    """
    Render a page header.
    
    Args:
        title: Page title
        subtitle: Optional subtitle
    """
    st.markdown(
        f"""
        <div style="margin-bottom: 32px;">
            <h1 style="font-size: 32px; font-weight: 700; color: var(--text); margin-bottom: 8px;">
                {title}
            </h1>
            {f'<p style="font-size: 16px; color: var(--text-secondary);">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = ""):
    """
    Render a section header.
    
    Args:
        title: Section title
        subtitle: Optional subtitle
    """
    st.markdown(
        f"""
        <div style="margin: 32px 0 16px 0;">
            <h2 style="font-size: 24px; font-weight: 600; color: var(--text); margin-bottom: 4px;">
                {title}
            </h2>
            {f'<p style="font-size: 14px; color: var(--text-secondary);">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def divider(margin: str = "24px"):
    """
    Render a visual divider.
    
    Args:
        margin: CSS margin value
    """
    st.markdown(
        f"""
        <div style="
            height: 1px;
            background: var(--border);
            margin: {margin} 0;
        "></div>
        """,
        unsafe_allow_html=True,
    )


def spacer(height: str = "24px"):
    """
    Add vertical spacing.
    
    Args:
        height: CSS height value
    """
    st.markdown(
        f'<div style="height: {height};"></div>',
        unsafe_allow_html=True,
    )


def centered_container(content_html: str, max_width: str = "800px"):
    """
    Render centered content container.
    
    Args:
        content_html: HTML content to center
        max_width: Maximum width of container
    """
    st.markdown(
        f"""
        <div style="
            max-width: {max_width};
            margin: 0 auto;
        ">
            {content_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
