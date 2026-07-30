import io
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from src import config


def load_document(file_path: str = config.DATA_FILE_PATH):
    """Load a .txt file and return it as a list of LangChain Document objects."""
    loader = TextLoader(file_path, encoding="utf-8")
    return loader.load()


def load_document_from_bytes(file_bytes: bytes, filename: str) -> list[Document]:
    """Load document from uploaded byte content (.txt, .md, .pdf)."""
    filename_lower = filename.lower()
    
    if filename_lower.endswith(".pdf"):
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            documents = []
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    documents.append(Document(page_content=text, metadata={"source": filename, "page": idx + 1}))
            if documents:
                return documents
        except Exception as e:
            print(f"Warning: Failed to parse PDF with pypdf: {e}")

    # Fallback / Text / Markdown handling
    try:
        text_content = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text_content = file_bytes.decode("latin-1", errors="ignore")

    return [Document(page_content=text_content, metadata={"source": filename})]