"""
Utility for extracting plain text from HTML content.
Used to create AI-friendly text versions of blog posts.
"""

from bs4 import BeautifulSoup
import re


def extract_text_from_html(html_content: str) -> str:
    """
    Extract clean plain text from HTML content.

    Removes HTML tags, scripts, styles, and excessive whitespace
    while preserving paragraph structure for readability.

    Args:
        html_content: Raw HTML string

    Returns:
        Clean plain text suitable for AI consumption
    """
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for element in soup(['script', 'style', 'head', 'meta']):
        element.decompose()

    # Get text content
    text = soup.get_text(separator='\n')

    # Clean up whitespace
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line:  # Skip empty lines
            lines.append(line)

    # Join lines with newlines, collapsing multiple consecutive newlines
    text = '\n'.join(lines)

    # Replace multiple consecutive newlines with double newline (paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def extract_title_from_html(html_content: str) -> str:
    """
    Extract title from HTML content.

    Looks for <title>, <h1>, or first header tag.

    Args:
        html_content: Raw HTML string

    Returns:
        Extracted title or empty string if not found
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Try to find title tag
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text().strip()

    # Try to find h1 tag
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.get_text().strip()

    # Try to find first header tag (h2, h3, etc.)
    for i in range(2, 7):
        header_tag = soup.find(f'h{i}')
        if header_tag:
            return header_tag.get_text().strip()

    return ""


def extract_excerpt_from_text(text: str, max_length: int = 200) -> str:
    """
    Extract an excerpt from plain text.

    Takes the first paragraph or first N characters.

    Args:
        text: Plain text string
        max_length: Maximum length of excerpt

    Returns:
        Excerpt string
    """
    # Try to get first paragraph
    paragraphs = text.split('\n\n')
    first_para = paragraphs[0] if paragraphs else text

    # Truncate if too long
    if len(first_para) > max_length:
        # Find last space before max_length
        truncated = first_para[:max_length]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        return truncated + '...'

    return first_para
