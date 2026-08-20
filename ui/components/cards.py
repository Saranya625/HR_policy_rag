"""Card components for displaying information."""

import streamlit as st
from typing import Optional


def feature_card(title: str, description: str, icon: Optional[str] = None):
    """Render a feature card using Streamlit."""

    icon_html = (
        f'<div style="font-size:32px; margin-bottom:16px;">{icon}</div>'
        if icon
        else ""
    )

    html = (
        '<div style="'
        'background:var(--surface);'
        'border:1px solid var(--border);'
        'border-radius:var(--radius-lg);'
        'padding:28px;'
        'text-align:center;'
        'height:100%;'
        '">'
        f'{icon_html}'
        f'<div style="font-size:18px;font-weight:600;color:var(--text);'
        f'margin-bottom:12px;">{title}</div>'
        f'<div style="font-size:14px;color:var(--text-secondary);'
        f'line-height:1.6;">{description}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)

def info_card(
    title: str,
    content: str,
    status: Optional[str] = None,
    status_type: str = "success",
):
    """Render an information card with optional status."""
    status_colors = {
        "success": "background: #D1FAE5; color: #10B981;",
        "warning": "background: #FEF3C7; color: #F59E0B;",
        "info": "background: #DBEAFE; color: #2563EB;",
    }
    
    status_html = ""
    if status:
        status_style = status_colors.get(status_type, status_colors["info"])
        status_html = f'<span style="display: inline-flex; align-items: center; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 500; {status_style}">{status}</span>'
    
    st.markdown(
        f"""
        <div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 20px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                <div style="font-size: 16px; font-weight: 600; color: #111827;">{title}</div>
                {status_html}
            </div>
            <div style="font-size: 15px; color: #6B7280; line-height: 1.6;">{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def stat_card(label: str, value: str, sublabel: Optional[str] = None):
    """Render a statistics card."""
    sublabel_html = (
        f'<p style="font-size: 13px; color: var(--text-muted); margin-top: 4px;">{sublabel}</p>'
        if sublabel
        else ""
    )
    
    st.markdown(
        f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 32px; font-weight: 700; color: var(--primary); margin-bottom: 8px;">
                {value}
            </div>
            <div style="font-size: 14px; font-weight: 500; color: var(--text);">
                {label}
            </div>
            {sublabel_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def document_card(
    filename: str,
    chunks: int,
    status: str = "Active",
    show_actions: bool = True,
):
    """Render a document information card."""
    st.markdown(
        f"""
        <div class="card">
            <div style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h3 style="font-size: 18px; font-weight: 600; color: var(--text);">
                        {filename}
                    </h3>
                    <span class="status-pill status-success">{status}</span>
                </div>
                <p style="font-size: 13px; color: var(--text-muted);">
                    {chunks} chunks indexed
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if show_actions:
        cols = st.columns([1, 1, 2])
        with cols[0]:
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            replace = st.button("Replace", key="doc_replace", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            delete = st.button("Reset", key="doc_delete", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        return replace, delete
    
    return False, False
