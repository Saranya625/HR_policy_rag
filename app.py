"""Streamlit chat app for the HR Policy Assistant."""

from html import escape

import streamlit as st
from src.pipeline import ask, build_hr_assistant, build_hr_assistant_from_upload

# Page Configuration
st.set_page_config(
    page_title="HR Policy Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for a premium single-page AI workspace.
CUSTOM_CSS = """
<style>
:root {
    color-scheme: light;
    --bg: #FCFCFD;
    --card: #FFFFFF;
    --card-soft: #F7F7F8;
    --text: #111111;
    --muted: #6B7280;
    --muted-strong: #374151;
    --border: #ECECEC;
    --border-strong: #D8DADC;
    --accent: #111111;
    --accent-hover: #2563EB;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 18px;
    --shadow-sm: 0 1px 2px rgba(17, 17, 17, 0.04);
    --shadow-md: 0 16px 50px rgba(17, 17, 17, 0.06);
    --shadow-float: 0 18px 60px rgba(17, 17, 17, 0.12);
    --shadow-focus: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", sans-serif !important;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

*, *::before, *::after {
    box-sizing: border-box;
}

.stApp *,
.main *,
[data-testid="stAppViewContainer"] * {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", sans-serif !important;
}

h1, h2, h3, h4, h5, h6, p, span, label, small, li, div {
    color: inherit;
}

header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
#MainMenu,
footer {
    display: none !important;
}

.main .block-container {
    max-width: 980px !important;
    padding: 96px 32px 120px !important;
}

.app-shell {
    min-height: calc(100vh - 216px);
}
.top-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    height: 64px;
    padding: 0 max(32px, calc((100vw - 980px) / 2 + 32px));
    background: rgba(252, 252, 253, 0.86);
    border-bottom: 1px solid rgba(236, 236, 236, 0.84);
    backdrop-filter: blur(18px);
}
.nav-brand {
    color: var(--text) !important;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0;
}
.source-pill {
    display: inline-flex;
    align-items: center;
    max-width: 46vw;
    min-height: 30px;
    padding: 6px 11px;
    color: var(--muted-strong) !important;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 999px;
    box-shadow: var(--shadow-sm);
    font-size: 13px;
    font-weight: 500;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.source-dot {
    width: 7px;
    height: 7px;
    margin-right: 8px;
    background: #22C55E;
    border-radius: 999px;
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.12);
    flex: 0 0 auto;
}
.intro {
    min-height: 108px;
    margin-bottom: 8px;
}
.intro-title {
    margin: 0 0 8px;
    color: var(--text) !important;
    font-size: 36px;
    font-weight: 650;
    line-height: 1.12;
    letter-spacing: 0;
}
.intro-copy {
    max-width: 620px;
    margin: 0;
    color: var(--muted) !important;
    font-size: 15px;
    line-height: 1.6;
}
.section-title {
    margin: 0 !important;
    color: var(--text) !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    letter-spacing: 0;
}
.section-subtitle,
.meta-text {
    color: var(--muted) !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}
.kb-card {
    margin: 0 0 18px;
    padding: 18px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
}
.kb-card:hover {
    border-color: var(--border-strong);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}
.kb-grid {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
}
.kb-main {
    min-width: 0;
}
.kb-label {
    margin: 0 0 7px;
    color: var(--muted) !important;
    font-size: 13px;
    line-height: 1.3;
}
.kb-name {
    margin: 0;
    color: var(--text) !important;
    font-size: 17px;
    font-weight: 600;
    line-height: 1.35;
    overflow-wrap: anywhere;
}
.kb-meta {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}
.kb-actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: 8px;
}
.tab-intro {
    margin: 0 0 22px;
}
.tab-title {
    margin: 0 0 6px;
    color: var(--text) !important;
    font-size: 20px;
    font-weight: 600;
    line-height: 1.3;
}
.tab-copy {
    max-width: 620px;
    margin: 0;
    color: var(--muted) !important;
    font-size: 13px;
    line-height: 1.6;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    min-height: 26px;
    padding: 5px 10px;
    border-radius: 999px;
    color: var(--muted-strong) !important;
    background: #F8F8F9;
    border: 1px solid var(--border);
    font-size: 12px;
    font-weight: 500;
    line-height: 1.25;
}
.status-ready {
    color: #166534 !important;
    background: #F0FDF4;
    border-color: #DCFCE7;
}
.upload-panel {
    margin-top: 18px;
    padding-top: 18px;
    border-top: 1px solid var(--border);
    animation: fadeIn 180ms ease both;
}
.upload-title {
    margin: 0 0 6px;
    color: var(--text) !important;
    font-size: 14px;
    font-weight: 600;
}
.upload-copy {
    margin: 0 0 14px;
    color: var(--muted) !important;
    font-size: 13px;
    line-height: 1.55;
}

.chat-workspace {
    min-height: 56vh;
    margin-top: 0px;
}
.empty-chat {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    min-height: 22vh;
    padding: 12px 0;
}
.empty-title {
    margin: 0 0 10px;
    color: var(--text) !important;
    font-size: 28px;
    font-weight: 650;
    line-height: 1.2;
    letter-spacing: 0;
}
.example-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px 24px;
    max-width: 640px;
    margin: 0 0 12px;
    padding: 0;
    list-style: none;
}
.example-list li {
    color: var(--muted) !important;
    font-size: 15px;
    line-height: 1.6;
}
.prompt-row {
    margin-top: 2px;
}
.prompt-row [data-testid="column"] {
    min-width: fit-content;
}
.chat-transcript {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin: 0 0 14px;
    padding-bottom: 18px;
    animation: fadeIn 180ms ease both;
}

div[data-testid="stTabs"] [role="tablist"],
div[data-baseweb="tab-list"] {
    gap: 8px !important;
    margin: 0 0 28px !important;
    padding: 4px !important;
    background: #F4F4F5 !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    width: fit-content !important;
}

div[data-testid="stTabs"] [role="tab"],
button[data-baseweb="tab"] {
    min-height: 36px !important;
    padding: 8px 14px !important;
    color: var(--muted-strong) !important;
    -webkit-text-fill-color: var(--muted-strong) !important;
    background: transparent !important;
    border: 0 !important;
    border-radius: 999px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: color 180ms ease, background-color 180ms ease, box-shadow 180ms ease !important;
}

div[data-testid="stTabs"] [role="tab"]:hover,
button[data-baseweb="tab"]:hover {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    background: rgba(255, 255, 255, 0.72) !important;
}

div[data-testid="stTabs"] [role="tab"][aria-selected="true"],
button[aria-selected="true"] {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    background: #FFFFFF !important;
    box-shadow: var(--shadow-sm) !important;
}

div[data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    display: none !important;
}

.stButton button {
    min-height: 40px !important;
    padding: 9px 15px !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    box-shadow: none !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: color 180ms ease, background-color 180ms ease, border-color 180ms ease, transform 180ms ease, box-shadow 180ms ease !important;
}
.stButton button:hover {
    color: var(--accent-hover) !important;
    -webkit-text-fill-color: var(--accent-hover) !important;
    background: #FFFFFF !important;
    border-color: var(--border-strong) !important;
    box-shadow: var(--shadow-sm) !important;
    transform: translateY(-1px);
}
.stButton button:focus-visible,
div[data-testid="stChatInput"]:focus-within,
section[data-testid="stFileUploadDropzone"]:focus-within {
    outline: 2px solid rgba(37, 99, 235, 0.6) !important;
    outline-offset: 3px !important;
}
.stButton button * {
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
}
.primary-action button {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}
.primary-action button:hover {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background: #1F2937 !important;
    border-color: #1F2937 !important;
}
.prompt-pill button {
    min-height: 36px !important;
    padding: 8px 13px !important;
    background: #FFFFFF !important;
    border-color: var(--border) !important;
    color: var(--muted-strong) !important;
    -webkit-text-fill-color: var(--muted-strong) !important;
}

div[data-testid="stChatMessage"] {
    padding: 4px 0 !important;
    background: transparent !important;
}
div[data-testid="stChatMessageAvatar"],
div[data-testid="chatAvatarIcon-user"],
div[data-testid="chatAvatarIcon-assistant"],
div[data-testid="stChatMessage"] [data-testid*="Avatar"],
div[data-testid="stChatMessage"] [class*="avatar"],
div[data-testid="stChatMessage"] [class*="Avatar"] {
    display: none !important;
}
div[data-testid="stChatMessage"] > div:first-child {
    width: 0 !important;
    min-width: 0 !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
}
div[data-testid="stChatMessage"] > div:first-child * {
    display: none !important;
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
}
div[data-testid="stChatMessageContent"] {
    width: fit-content !important;
    max-width: min(760px, 88%) !important;
    padding: 17px 19px !important;
    color: var(--text) !important;
    background: var(--card) !important;
    border: 0 !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 26px rgba(17, 17, 17, 0.06) !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]) {
    display: flex !important;
    width: 100% !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) div[data-testid="stChatMessageContent"],
div[data-testid="stChatMessage"]:has([aria-label="user avatar"]) div[data-testid="stChatMessageContent"] {
    margin-left: auto !important;
    background: #F3F4F6 !important;
    box-shadow: none !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) div[data-testid="stChatMessageContent"],
div[data-testid="stChatMessage"]:has([aria-label="assistant avatar"]) div[data-testid="stChatMessageContent"] {
    margin-right: auto !important;
}
div[data-testid="stChatMessageContent"] * {
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
}

div[data-testid="stChatInput"] {
    width: min(916px, calc(100vw - 64px)) !important;
    min-height: 64px;
    margin: 0 auto 24px !important;
    background: transparent !important;
    border: 0 !important;
    border-radius: 24px !important;
    box-shadow: none !important;
}
div[data-testid="stChatInput"] > div {
    min-height: 64px !important;
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 24px !important;
    box-shadow: var(--shadow-float) !important;
    transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease !important;
}
div[data-testid="stChatInput"]:focus-within > div {
    border-color: rgba(37, 99, 235, 0.42) !important;
    box-shadow: var(--shadow-focus), var(--shadow-float) !important;
    transform: translateY(-1px);
}
div[data-testid="stChatInput"] textarea {
    min-height: 62px !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
    padding-top: 20px !important;
    padding-bottom: 18px !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--muted) !important;
    -webkit-text-fill-color: var(--muted) !important;
    opacity: 1;
}
div[data-testid="stChatInput"] button {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background: var(--accent) !important;
    border: 0 !important;
    border-radius: 999px !important;
    box-shadow: none !important;
    transition: background-color 180ms ease, transform 180ms ease !important;
}
div[data-testid="stChatInput"] button:hover {
    background: var(--accent-hover) !important;
    transform: translateY(-1px);
}
div[data-testid="stChatInput"] button svg {
    fill: currentColor !important;
    color: currentColor !important;
}

section[data-testid="stFileUploadDropzone"] {
    padding: 20px !important;
    color: var(--text) !important;
    background: #FAFAFA !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: none !important;
    transition: border-color 180ms ease, background-color 180ms ease !important;
}
div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploader"] section > div,
div[data-testid="stFileUploader"] [data-testid="stFileUploadDropzone"],
div[data-testid="stFileUploader"] [data-testid="stFileUploadDropzone"] > div,
div[data-testid="stFileUploader"] [data-testid="stFileUploadDropzone"] [data-testid],
div[data-testid="stFileUploaderDropzone"],
div[data-testid="stFileUploaderDropzone"] > div {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    background: #FAFAFA !important;
    border-color: var(--border) !important;
}
section[data-testid="stFileUploadDropzone"]:hover {
    background: var(--card) !important;
    border-color: var(--border-strong) !important;
}
div[data-testid="stFileUploader"] button,
div[data-testid="stFileUploader"] button[kind],
section[data-testid="stFileUploadDropzone"] button[kind] {
    min-height: 40px !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    box-shadow: none !important;
}
div[data-testid="stFileUploader"] button:hover,
section[data-testid="stFileUploadDropzone"] button:hover {
    border-color: var(--border-strong) !important;
    background: var(--bg) !important;
}

div[data-testid="stFileUploader"] label,
div[data-testid="stFileUploader"] p,
div[data-testid="stFileUploader"] span {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}

div[data-testid="stSpinner"] *,
div[data-testid="stAlert"] *,
div[data-testid="stToast"] * {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}

[data-testid="stMarkdownContainer"] p {
    color: inherit;
    line-height: inherit;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 640px) {
    .main .block-container { padding: 80px 16px 112px !important; }
    .top-nav {
        height: 60px;
        padding: 0 16px;
    }
    .source-pill {
        max-width: 54vw;
        font-size: 12px;
    }
    div[data-testid="stTabs"] [role="tablist"],
    div[data-baseweb="tab-list"] {
        width: 100% !important;
        overflow-x: auto !important;
    }
    .intro {
        min-height: 96px;
    }
    .intro-title {
        font-size: 30px;
    }
    .kb-grid {
        align-items: flex-start;
        flex-direction: column;
        gap: 16px;
    }
    .kb-actions {
        justify-content: flex-start;
    }
    .example-list {
        grid-template-columns: 1fr;
        gap: 6px;
    }
    div[data-testid="stChatMessageContent"] {
        max-width: 94% !important;
    }
    div[data-testid="stChatInput"] {
        width: calc(100vw - 24px) !important;
        margin-bottom: 14px !important;
    }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Lazy Assistant Loader
@st.cache_resource(show_spinner=False)
def load_default_assistant():
    return build_hr_assistant()


# Session State Initialization
if "active_doc_name" not in st.session_state:
    st.session_state.active_doc_name = "Default HR Policy"
    st.session_state.is_custom_doc = False
    st.session_state.active_chunk_count = None
    st.session_state.agent = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_upload" not in st.session_state:
    st.session_state.show_upload = False

if st.session_state.agent is None:
    with st.spinner("Preparing assistant..."):
        st.session_state.agent = load_default_assistant()


active_doc_display = (
    st.session_state.active_doc_name if st.session_state.is_custom_doc else "Company HR Policy"
)
safe_active_doc = escape(active_doc_display)
chunk_count = st.session_state.active_chunk_count
chunk_label = f"{chunk_count} chunks" if chunk_count else "Default index"
status_label = "Indexed successfully" if st.session_state.is_custom_doc else "Ready"

st.markdown(
    f"""
    <div class="top-nav">
        <div class="nav-brand">HR Intelligence</div>
        <div class="source-pill" title="{safe_active_doc}">
            <span class="source-dot"></span>
            <span>{safe_active_doc}</span>
        </div>
    </div>
    <main class="app-shell">
        <section class="intro">
            <h1 class="intro-title">HR Intelligence</h1>
            <p class="intro-copy">AI assistant for company policies. Grounded answers from your HR documents.</p>
        </section>
    </main>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <section class="kb-card">
        <div class="kb-grid">
            <div class="kb-main">
                <p class="kb-label">Current Knowledge Base</p>
                <h2 class="kb-name">{safe_active_doc}</h2>
                <div class="kb-meta">
                    <span class="status-pill status-ready">{status_label}</span>
                    <span class="status-pill">{chunk_label}</span>
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

action_cols = st.columns([1, 1, 5])
with action_cols[0]:
    st.markdown('<div class="primary-action">', unsafe_allow_html=True)
    if st.button("Replace Document", key="toggle_upload"):
        st.session_state.show_upload = not st.session_state.show_upload
    st.markdown("</div>", unsafe_allow_html=True)

with action_cols[1]:
    if st.button("Reset", key="reset_default_policy"):
        st.session_state.agent = load_default_assistant()
        st.session_state.active_doc_name = "Default HR Policy"
        st.session_state.is_custom_doc = False
        st.session_state.active_chunk_count = None
        st.session_state.last_uploaded_name = None
        st.session_state.messages = []
        st.session_state.show_upload = False
        st.toast("Restored default HR policy.")
        st.rerun()

if st.session_state.show_upload:
    st.markdown(
        """
        <div class="upload-panel">
            <p class="upload-title">Replace knowledge base</p>
            <p class="upload-copy">Upload a text, markdown, or PDF policy document. It will become the active source for this chat.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Upload custom HR document",
        type=["txt", "md", "pdf"],
        help="Upload your policy or handbook to build an active vector index.",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        if st.session_state.get("last_uploaded_name") != uploaded_file.name:
            with st.spinner("Indexing document..."):
                file_bytes = uploaded_file.getvalue()
                new_agent, chunk_count = build_hr_assistant_from_upload(file_bytes, uploaded_file.name)

                st.session_state.agent = new_agent
                st.session_state.active_doc_name = uploaded_file.name
                st.session_state.is_custom_doc = True
                st.session_state.active_chunk_count = chunk_count
                st.session_state.last_uploaded_name = uploaded_file.name
                st.session_state.messages = []
                st.session_state.show_upload = False
                st.toast(f"Indexed {uploaded_file.name} successfully.")
                st.rerun()

st.markdown('<section class="chat-workspace">', unsafe_allow_html=True)

prompt_clicked = None
if not st.session_state.messages:
    st.markdown(
        """
        <div class="empty-chat">
            <h2 class="empty-title">What would you like to know?</h2>
            <ul class="example-list">
                <li>Can I work remotely?</li>
                <li>How many sick leaves do I get?</li>
                <li>What is the notice period?</li>
                <li>Explain maternity policy.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="prompt-row">', unsafe_allow_html=True)
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        st.markdown('<div class="prompt-pill">', unsafe_allow_html=True)
        if st.button("What is the WFH policy?", key="prompt_wfh"):
            prompt_clicked = "What is the Work From Home (WFH) policy?"
        st.markdown("</div>", unsafe_allow_html=True)
    with p_col2:
        st.markdown('<div class="prompt-pill">', unsafe_allow_html=True)
        if st.button("How many leave days?", key="prompt_leave"):
            prompt_clicked = "How many leave days am I allowed per year?"
        st.markdown("</div>", unsafe_allow_html=True)
    with p_col3:
        st.markdown('<div class="prompt-pill">', unsafe_allow_html=True)
        if st.button("Notice period", key="prompt_notice"):
            prompt_clicked = "What is the notice period policy?"
        st.markdown("</div>", unsafe_allow_html=True)
    with p_col4:
        st.markdown('<div class="prompt-pill">', unsafe_allow_html=True)
        if st.button("Insurance policy", key="prompt_insurance"):
            prompt_clicked = "What is the insurance policy?"
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if prompt_clicked:
    st.session_state.messages.append({"role": "user", "content": prompt_clicked})
    with st.spinner("Generating answer..."):
        try:
            ans = ask(st.session_state.agent, prompt_clicked)
        except Exception as e:
            ans = f"An error occurred while processing your request: {e}"
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.rerun()

if st.session_state.messages:
    st.markdown('<div class="chat-transcript">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</section>", unsafe_allow_html=True)

user_query = st.chat_input("Ask a question about your company policies...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            try:
                answer = ask(st.session_state.agent, user_query)
            except Exception as e:
                answer = f"An error occurred while processing your request: {e}"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
