"""Landing page component."""

import streamlit as st
from ui.components.cards import feature_card
from ui.components.layout import spacer


def render_landing_page():
    """Render the landing/welcome page."""
    
    # Hero Section
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 64px 0;
            max-width: 800px;
            margin: 0 auto;
        ">
            <h1 style="
                font-size: 48px;
                font-weight: 700;
                color: var(--text);
                margin-bottom: 24px;
                line-height: 1.2;
            ">
                HR Intelligence
            </h1>
            <p style="
                font-size: 20px;
                color: var(--text-secondary);
                line-height: 1.6;
                margin-bottom: 40px;
            ">
                Your AI-powered HR policy assistant. Get instant answers from your company documents 
                using advanced retrieval and natural language understanding.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        get_started = st.button(
            "Get Started",
            key="landing_cta",
            use_container_width=True,
            type="primary",
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    spacer("64px")
    
    # Feature Cards
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 48px;">
            <h2 style="
                font-size: 32px;
                font-weight: 700;
                color: var(--text);
                margin-bottom: 16px;
            ">
                Powerful Features
            </h2>
            <p style="
                font-size: 16px;
                color: var(--text-secondary);
            ">
                Everything you need for intelligent HR document assistance
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        feature_card(
            title="Semantic Search",
            description="Advanced vector search finds relevant information across your entire HR knowledge base.",
        )
    
    with col2:
        feature_card(
            title="Custom Documents",
            description="Upload your own policies and handbooks to create a personalized knowledge base.",
        )
    
    with col3:
        feature_card(
            title="Grounded Answers",
            description="AI responses are grounded in your actual documents, ensuring accuracy and relevance.",
        )
    
    spacer("64px")
    
    # How it Works Section
    st.markdown(
        """
        <div style="
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 48px;
            text-align: center;
        ">
            <h2 style="
                font-size: 28px;
                font-weight: 700;
                color: var(--text);
                margin-bottom: 24px;
            ">
                How It Works
            </h2>
            <div style="
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 32px;
                margin-top: 32px;
            ">
                <div>
                    <div style="
                        width: 56px;
                        height: 56px;
                        background: var(--primary-light);
                        color: var(--primary);
                        border-radius: var(--radius-full);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        font-weight: 700;
                        margin: 0 auto 16px;
                    ">1</div>
                    <h3 style="
                        font-size: 18px;
                        font-weight: 600;
                        color: var(--text);
                        margin-bottom: 8px;
                    ">Upload Documents</h3>
                    <p style="
                        font-size: 14px;
                        color: var(--text-secondary);
                        line-height: 1.5;
                    ">Add your HR policies and handbooks</p>
                </div>
                <div>
                    <div style="
                        width: 56px;
                        height: 56px;
                        background: var(--primary-light);
                        color: var(--primary);
                        border-radius: var(--radius-full);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        font-weight: 700;
                        margin: 0 auto 16px;
                    ">2</div>
                    <h3 style="
                        font-size: 18px;
                        font-weight: 600;
                        color: var(--text);
                        margin-bottom: 8px;
                    ">Ask Questions</h3>
                    <p style="
                        font-size: 14px;
                        color: var(--text-secondary);
                        line-height: 1.5;
                    ">Chat naturally about any HR topic</p>
                </div>
                <div>
                    <div style="
                        width: 56px;
                        height: 56px;
                        background: var(--primary-light);
                        color: var(--primary);
                        border-radius: var(--radius-full);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        font-weight: 700;
                        margin: 0 auto 16px;
                    ">3</div>
                    <h3 style="
                        font-size: 18px;
                        font-weight: 600;
                        color: var(--text);
                        margin-bottom: 8px;
                    ">Get Answers</h3>
                    <p style="
                        font-size: 14px;
                        color: var(--text-secondary);
                        line-height: 1.5;
                    ">Receive accurate, source-backed responses</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    return get_started
