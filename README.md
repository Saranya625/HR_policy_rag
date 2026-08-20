# HR Policy RAG Assistant

A retrieval-augmented generation (RAG) assistant that answers questions about a company HR policy document. It searches the handbook for relevant passages, then uses a Groq-hosted language model to produce a grounded response.

The repository includes both a command-line demo and a Streamlit chat interface. The bundled policy is a fictional Acme Corp handbook intended for demonstration.

## Features

- Loads and splits the HR policy text into overlapping chunks.
- Creates semantic embeddings with Jina and stores them in a local FAISS index.
- Reuses the saved index on later runs, avoiding repeated embedding work.
- Retrieves the three most relevant policy chunks for each question.
- Uses a LangChain agent instructed to search the policy before answering and to avoid guessing when the information is unavailable.
- Provides a CLI demo and a browser-based chat UI.

## Tech stack

- Python
- LangChain and LangChain Community
- Groq (`openai/gpt-oss-20b`) for chat completion
- Jina (`jina-embeddings-v2-base-en`) for embeddings
- FAISS for local vector search
- Streamlit for the web interface

## Project structure

```text
.
|-- app.py                 # Streamlit chat application
|-- main.py                # Command-line demo
|-- data/
|   `-- hr_policy.txt      # Source policy document
|-- src/
|   |-- pipeline.py        # Builds the end-to-end assistant
|   |-- document_loader.py # Reads the policy document
|   |-- splitter.py        # Splits text into chunks
|   |-- embeddings.py      # Jina embedding model
|   |-- vector_store.py    # FAISS index creation and persistence
|   |-- tool.py            # HR-policy retrieval tool
|   |-- llm.py             # Groq chat model
|   |-- agent.py           # LangChain agent configuration
|   `-- config.py          # Settings, paths, and environment checks
`-- requirements.txt
```

## Prerequisites

- Python 3.10 or newer
- A [Groq API key](https://console.groq.com/keys)
- A [Jina AI API key](https://jina.ai/api-dashboard/)

## Setup

1. Clone the repository and enter it.

   ```bash
   git clone <repository-url>
   cd HR_policy_rag
   ```

2. Create and activate a virtual environment.

   ```bash
   python -m venv rag_env
   # Windows PowerShell
   .\rag_env\Scripts\Activate.ps1
   # macOS/Linux
   source rag_env/bin/activate
   ```

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root.

   ```env
   GROQ_API_KEY=your_groq_api_key
   JINA_API_KEY=your_jina_api_key
   ```

   `.env` is ignored by Git, so credentials are kept out of version control.

## Run the app

### Streamlit chat interface

```bash
E:\project\rag_env\Scripts\python.exe -m streamlit run app.py
```

Streamlit opens the HR Policy Assistant in your browser. Ask questions such as:

- `How many paid annual leave days do I get?`
- `What is the notice period during probation?`
- `Can I work from home every day?`

### Command-line demo

```bash
python main.py
```

This builds the assistant and runs a few sample questions.

## How it works

```text
data/hr_policy.txt
        |
        v
Load and split text (500-character chunks, 60-character overlap)
        |
        v
Jina embeddings -> local FAISS index
        |
        v
Retrieve top 3 relevant chunks for each question
        |
        v
Groq LLM agent -> grounded answer
```

On the first run, the app creates `data/faiss_index/`. Later runs load that index instead of embedding the document again.

## Use your own policy document

1. Replace the contents of `data/hr_policy.txt` with your policy in UTF-8 plain-text format.
2. Remove `data/faiss_index/` so the next launch rebuilds the index for the updated document.
3. Run either interface again.

The source document is intentionally separate from the application code, so this is the simplest way to tailor the assistant. If you move or rename the document, update `DATA_FILE_PATH` in `src/config.py`.

## Configuration

The main settings live in `src/config.py`:

| Setting | Default | Purpose |
| --- | --- | --- |
| `LLM_MODEL_NAME` | `openai/gpt-oss-20b` | Groq chat model |
| `EMBEDDING_MODEL_NAME` | `jina-embeddings-v2-base-en` | Embedding model |
| `CHUNK_SIZE` | `500` | Maximum chunk size in characters |
| `CHUNK_OVERLAP` | `60` | Context shared by adjacent chunks |
| `TOP_K_RESULTS` | `3` | Number of chunks returned by search |

## Notes

- The assistant is only as accurate as the provided policy document; it should not replace HR or legal guidance.
- The saved FAISS index is loaded with deserialization enabled because it is generated locally by this app. Do not load an index from an untrusted source.
- The current document and UI are demo-oriented; adapt the source policy and branding before production use.


