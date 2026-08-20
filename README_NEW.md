# HR Intelligence - Architecture Documentation

## Overview

HR Intelligence is a production-ready AI-powered HR policy assistant built with Streamlit, LangChain, and modern UI/UX principles. The application has been completely refactored with a modular, maintainable frontend architecture.

## Project Structure

```
project/
├── app.py                      # Main application entry point and router
├── main.py                     # CLI demo (unchanged)
├── requirements.txt            # Python dependencies
│
├── src/                        # Backend (RAG pipeline - unchanged)
│   ├── agent.py               # LangChain agent configuration
│   ├── config.py              # Configuration and environment
│   ├── document_loader.py     # Document loading utilities
│   ├── embeddings.py          # Embedding model setup
│   ├── llm.py                 # LLM configuration
│   ├── pipeline.py            # Main RAG pipeline
│   ├── splitter.py            # Document chunking
│   ├── tool.py                # LangChain tools
│   └── vector_store.py        # FAISS vector store
│
├── ui/                         # Frontend modules (NEW)
│   ├── __init__.py
│   ├── theme.py               # Design system and theme constants
│   ├── styles.css             # Global CSS styles
│   │
│   ├── components/            # Reusable UI components
│   │   ├── __init__.py
│   │   ├── navbar.py          # Navigation bar component
│   │   ├── cards.py           # Card components (feature, info, stat, document)
│   │   ├── chat.py            # Chat interface components
│   │   └── layout.py          # Layout utilities and helpers
│   │
│   └── pages/                 # Page modules
│       ├── __init__.py
│       ├── landing.py         # Landing/welcome page
│       ├── overview.py        # Dashboard/overview page
│       ├── documents.py       # Document upload page
│       └── assistant.py       # AI chat assistant page
│
├── utils/                      # Utility functions (NEW)
│   ├── __init__.py
│   ├── session.py             # Session state management
│   └── formatters.py          # Text formatting utilities
│
└── data/                       # Data files
    ├── hr_policy.txt          # Default HR policy
    └── faiss_index/           # Vector store cache
```

## Application Flow

### 1. Landing Page (`ui/pages/landing.py`)
- Hero section with product introduction
- Feature cards showcasing capabilities
- "How it Works" section
- Primary CTA: "Get Started" button

### 2. Overview Page (`ui/pages/overview.py`)
- Dashboard with key statistics
- Knowledge base status and information
- Quick action buttons
- Recent conversation activity
- System status indicators

### 3. Documents Page (`ui/pages/documents.py`)
- Centered document upload interface
- Drag-and-drop file support
- Active document information
- Document management actions
- Format guidelines and tips

### 4. Assistant Page (`ui/pages/assistant.py`)
- ChatGPT-style conversation interface
- Suggested prompts when empty
- Streaming responses with typing cursor
- Message history with proper alignment
- Clear chat functionality

## Design System

### Color Palette
```python
Background:      #FAFAFA
Surface:         #FFFFFF
Border:          #E5E7EB
Text:            #111827
Text Secondary:  #6B7280
Primary:         #2563EB
Success:         #10B981
Warning:         #F59E0B
Danger:          #EF4444
```

### Spacing System (8px base)
```python
xs:  4px
sm:  8px
md:  16px
lg:  24px
xl:  32px
2xl: 48px
3xl: 64px
```

### Typography
```python
H1:      32px / 700 weight
H2:      24px / 600 weight
H3:      18px / 600 weight
Body:    15px / 400 weight
Caption: 13px / 400 weight
```

### Component Styles
- **Cards**: White background, subtle border, rounded corners (12px), shadow on hover
- **Buttons**: Three variants (primary, secondary, danger), 40px height, full border radius
- **Chat Bubbles**: Max-width 680px, 16px padding, rounded corners, aligned by role
- **Input Fields**: 56px height, focus state with primary color, shadow effect

## Key Features

### 1. Modular Architecture
- Separated UI components from business logic
- Reusable components with clear interfaces
- Easy to maintain and extend
- Type hints for better code quality

### 2. Professional Design
- Modern, minimalist interface
- Consistent spacing and typography
- Smooth animations and transitions
- Responsive layout for all screen sizes

### 3. State Management
- Centralized session state handling
- Clear separation of concerns
- Utility functions for common operations
- Predictable state updates

### 4. Chat Interface
- Real-time message streaming
- Typing cursor animation
- Proper message alignment (user right, assistant left)
- Suggested prompts for new users
- Clear chat history management

### 5. Document Management
- Intuitive upload interface
- Real-time processing feedback
- Document status indicators
- Easy switching between documents

## Component API

### Cards (`ui/components/cards.py`)

```python
feature_card(title, description, icon=None)
# Display a feature card with optional icon

info_card(title, content, status=None, status_type="success")
# Display an information card with optional status pill

stat_card(label, value, sublabel=None)
# Display a statistic with large value

document_card(filename, chunks, status="Active", show_actions=True)
# Display document information with optional actions
```

### Chat (`ui/components/chat.py`)

```python
render_suggested_prompts(prompts: List[str]) -> Optional[str]
# Display suggested prompt buttons, returns selected prompt

stream_response(text: str, placeholder) -> None
# Stream text word-by-word with typing cursor

render_conversation(messages: List[Dict]) -> None
# Render complete conversation history
```

### Layout (`ui/components/layout.py`)

```python
load_css()
# Load custom CSS styles

page_header(title: str, subtitle: str = "")
# Render page title and subtitle

section_header(title: str, subtitle: str = "")
# Render section heading

spacer(height: str = "24px")
# Add vertical spacing
```

### Navigation (`ui/components/navbar.py`)

```python
render_navbar(pages: List[Tuple[str, str]], active_page: str)
# Render navigation bar with pills, returns selected page
```

## Session State Variables

```python
st.session_state.current_page           # Active page: "landing" | "overview" | "documents" | "assistant"
st.session_state.agent                  # LangChain agent instance
st.session_state.messages               # List of chat messages [{"role": str, "content": str}]
st.session_state.active_doc_name        # Current document filename
st.session_state.is_custom_doc          # Boolean: custom vs default document
st.session_state.active_chunk_count     # Number of indexed chunks
st.session_state.last_uploaded_name     # Last uploaded filename (prevents re-indexing)
```

## Running the Application

### Installation
```bash
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file with:
```
GROQ_API_KEY=your_api_key_here
```

### Run Application
```bash
streamlit run app.py
```

### Run CLI Demo
```bash
python main.py
```

## Customization Guide

### Adding a New Page

1. Create page module in `ui/pages/`:
```python
# ui/pages/mypage.py
def render_mypage():
    page_header("My Page", "Description")
    # Your page content
```

2. Import in `app.py`:
```python
from ui.pages.mypage import render_mypage
```

3. Add to navigation:
```python
pages = [
    ("Overview", "overview"),
    ("My Page", "mypage"),
    # ...
]
```

4. Add routing:
```python
elif st.session_state.current_page == "mypage":
    render_mypage()
```

### Adding a New Component

1. Create component in `ui/components/`:
```python
# ui/components/mycomponent.py
def my_component(param1, param2):
    st.markdown(f"""
        <div class="card">
            {param1} - {param2}
        </div>
    """, unsafe_allow_html=True)
```

2. Import where needed:
```python
from ui.components.mycomponent import my_component
```

### Modifying Theme

Edit `ui/theme.py` or `ui/styles.css`:
```python
# ui/theme.py
COLORS = {
    "primary": "#YOUR_COLOR",
    # ...
}
```

## Best Practices

1. **Keep components small**: Each component should have a single responsibility
2. **Use session state utilities**: Import from `utils/session.py` for consistent state management
3. **Follow spacing system**: Use theme constants for consistent spacing
4. **Type hints**: Add type hints to all function signatures
5. **Error handling**: Wrap backend calls in try-except blocks
6. **Loading states**: Show spinners during async operations
7. **User feedback**: Provide success/error messages for all actions

## Performance Optimization

- Agent is cached with `@st.cache_resource`
- Vector store is persisted to disk
- CSS is loaded once at startup
- Components render only when needed
- Session state prevents unnecessary recomputation

## Accessibility

- Semantic HTML structure
- Proper heading hierarchy
- Focus states on interactive elements
- High contrast color ratios
- Keyboard navigation support

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Future Enhancements

- [ ] Export conversation as PDF/Markdown
- [ ] Multiple document support
- [ ] User authentication
- [ ] Conversation history persistence
- [ ] Analytics dashboard
- [ ] Advanced search filters
- [ ] Document comparison
- [ ] API endpoint for programmatic access

## Troubleshooting

### CSS not loading
- Check `ui/styles.css` exists
- Verify path in `load_css()` function
- Clear browser cache

### State not persisting
- Check session state initialization in `app.py`
- Verify `st.rerun()` calls after state changes

### Upload not working
- Verify file type in `allowed_types`
- Check `src/document_loader.py` handles the format
- Ensure sufficient memory for large files

## License

[Your License Here]

## Contributors

[Your Name/Team]
