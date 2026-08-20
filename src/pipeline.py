"""
Wires all the components together into one ready-to-use agent.

This is the single entry point that main.py (CLI) and app.py
(Streamlit) both call.
"""

import traceback
from typing import Any, Iterator

from src import config
from src.agent import create_hr_agent
from src.document_loader import load_document
from src.llm import get_llm
from src.splitter import split_into_chunks
from src.tool import create_search_tool
from src.vector_store import (
    build_vector_store,
    get_retriever,
    load_vector_store,
    save_vector_store,
    vector_store_exists,
)


# ============================================================
# VECTOR STORE
# ============================================================

def build_vector_store_for_document(
    file_path: str = config.DATA_FILE_PATH,
):
    """
    Load + split + embed the document.

    Reuses a saved index if one already exists.
    """

    if vector_store_exists():

        print(
            "Found a saved vector store on disk, "
            "loading it (fast, no re-embedding)."
        )

        return load_vector_store()

    print(
        "No saved vector store found, "
        "building one from scratch..."
    )

    documents = load_document(file_path)

    chunks = split_into_chunks(documents)

    print(
        f"Loaded '{file_path}' "
        f"and split it into {len(chunks)} chunks."
    )

    vector_store = build_vector_store(chunks)

    save_vector_store(vector_store)

    print(
        "Vector store built and saved to disk "
        "for next time."
    )

    return vector_store


# ============================================================
# BUILD NORMAL HR ASSISTANT
# ============================================================

def build_hr_assistant(
    file_path: str = config.DATA_FILE_PATH,
):
    """
    Build the full RAG agent,
    ready to answer questions.
    """

    config.check_api_keys()

    vector_store = build_vector_store_for_document(
        file_path
    )

    retriever = get_retriever(
        vector_store
    )

    search_tool = create_search_tool(
        retriever
    )

    llm = get_llm()

    agent = create_hr_agent(
        llm,
        [search_tool],
    )

    return agent


# ============================================================
# BUILD ASSISTANT FROM UPLOADED DOCUMENT
# ============================================================

def build_hr_assistant_from_upload(
    file_bytes: bytes,
    filename: str,
):
    """
    Build a dynamic RAG agent for a user-uploaded
    custom HR document.
    """

    config.check_api_keys()

    from src.document_loader import (
        load_document_from_bytes,
    )

    documents = load_document_from_bytes(
        file_bytes,
        filename,
    )

    chunks = split_into_chunks(
        documents
    )

    vector_store = build_vector_store(
        chunks
    )

    retriever = get_retriever(
        vector_store
    )

    search_tool = create_search_tool(
        retriever
    )

    llm = get_llm()

    agent = create_hr_agent(
        llm,
        [search_tool],
    )

    return agent, len(chunks)


# ============================================================
# RESPONSE EXTRACTION
# ============================================================

def _extract_answer(
    response: Any,
) -> str:
    """
    Normalize responses from supported
    LangChain agent styles.
    """

    if isinstance(response, dict):

        # LangGraph / create_agent
        if (
            "messages" in response
            and response["messages"]
        ):

            final_message = response["messages"][-1]

            return getattr(
                final_message,
                "content",
                str(final_message),
            )

        # AgentExecutor
        if "output" in response:
            return response["output"]

    return str(response)


# ============================================================
# NORMAL ASK
# ============================================================

def ask(
    agent,
    question: str,
) -> str:
    """
    Run the agent normally and return
    the complete final answer.

    Used by CLI and non-streaming code.
    """

    print("=" * 60)
    print("Question:", question)
    print("Agent type:", type(agent))

    try:

        # ----------------------------------------------------
        # New LangChain create_agent()
        # ----------------------------------------------------

        if agent.__class__.__name__ != "AgentExecutor":

            response = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question,
                        }
                    ]
                }
            )

        # ----------------------------------------------------
        # Older AgentExecutor
        # ----------------------------------------------------

        else:

            response = agent.invoke(
                {
                    "input": question
                }
            )

        print("Raw response:", response)

        return _extract_answer(
            response
        )

    except Exception:

        traceback.print_exc()

        raise


# ============================================================
# STREAMING
# ============================================================

def ask_stream(
    agent,
    question: str,
) -> Iterator[str]:
    """
    Stream the assistant response token-by-token.
    """

    print("=" * 60)
    print("Streaming question:", question)
    print("Agent type:", type(agent))

    try:

        # ====================================================
        # NEW LANGCHAIN create_agent()
        # ====================================================

        if agent.__class__.__name__ != "AgentExecutor":

            stream = agent.stream(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question,
                        }
                    ]
                },
                stream_mode="messages",
            )

            for item in stream:

                # --------------------------------------------
                # messages mode normally returns:
                #
                # (message_chunk, metadata)
                # --------------------------------------------

                if not isinstance(item, tuple):
                    continue

                if len(item) != 2:
                    continue

                message_chunk, metadata = item

                # --------------------------------------------
                # Extract content
                # --------------------------------------------

                content = getattr(
                    message_chunk,
                    "content",
                    None,
                )

                if not content:
                    continue

                # --------------------------------------------
                # Plain string
                # --------------------------------------------

                if isinstance(content, str):

                    yield content

                    continue

                # --------------------------------------------
                # Structured content
                # --------------------------------------------

                if isinstance(content, list):

                    for block in content:

                        # Plain string block
                        if isinstance(block, str):

                            yield block

                            continue

                        # Dictionary content block
                        if isinstance(block, dict):

                            text = block.get("text")

                            if text:
                                yield str(text)

                            continue

                        # Object content block
                        text = getattr(
                            block,
                            "text",
                            None,
                        )

                        if text:
                            yield str(text)

            return

        # ====================================================
        # OLD AgentExecutor
        # ====================================================

        stream = agent.stream(
            {
                "input": question
            }
        )

        for event in stream:

            if not isinstance(event, dict):
                continue

            output = event.get("output")

            if output:
                yield str(output)

    except Exception:

        traceback.print_exc()

        raise