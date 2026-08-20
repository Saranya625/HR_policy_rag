"""Text formatting and display utilities."""

from html import escape
from typing import Optional


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + suffix


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def safe_html(text: str) -> str:
    """
    Escape HTML characters for safe display.
    
    Args:
        text: Text to escape
    
    Returns:
        HTML-safe text
    """
    return escape(text)


def format_chunk_count(count: Optional[int]) -> str:
    """
    Format chunk count for display.
    
    Args:
        count: Number of chunks
    
    Returns:
        Formatted string
    """
    if count is None or count == 0:
        return "No chunks"
    elif count == 1:
        return "1 chunk"
    else:
        return f"{count:,} chunks"


def format_message_preview(content: str, max_length: int = 80) -> str:
    """
    Format message content as a preview.
    
    Args:
        content: Message content
        max_length: Maximum preview length
    
    Returns:
        Preview text
    """
    # Remove extra whitespace
    preview = " ".join(content.split())
    return truncate_text(preview, max_length)
