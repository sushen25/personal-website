#!/usr/bin/env python3
"""
Import a Medium blog post HTML file into DynamoDB.

This script:
1. Takes a Medium HTML export file as input
2. Extracts title, date, tags, and content from the HTML
3. Optionally takes thumbnail URL and metadata as arguments
4. Generates a URL-friendly slug
5. Saves the post to DynamoDB

Usage:
    # Basic usage (interactive prompts)
    python scripts/import_medium_post.py path/to/medium-post.html

    # With all metadata provided
    python scripts/import_medium_post.py path/to/medium-post.html \\
        --title "My Blog Post" \\
        --slug "my-blog-post" \\
        --date "2025-01-21" \\
        --tags "Python,AWS,DynamoDB" \\
        --thumbnail "https://example.com/image.png" \\
        --status published

    # Use local DynamoDB
    python scripts/import_medium_post.py path/to/medium-post.html --local

    # Dry run to preview without saving
    python scripts/import_medium_post.py path/to/medium-post.html --dry-run
"""

import sys
import os
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from bs4 import BeautifulSoup
from src.utils.text_extractor import extract_text_from_html, extract_excerpt_from_text, extract_title_from_html
from src.utils.dynamodb import blog_db
from src.models.schemas import BlogPost


def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.

    Args:
        text: Text to convert

    Returns:
        URL-friendly slug
    """
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


def extract_medium_metadata(html_content: str) -> dict:
    """
    Extract metadata from Medium HTML export.

    Args:
        html_content: Raw HTML string

    Returns:
        Dictionary with extracted metadata
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata = {}

    # Extract title
    title_tag = soup.find('h1')
    if title_tag:
        metadata['title'] = title_tag.get_text().strip()
    else:
        # Fallback to title tag or first h2
        metadata['title'] = extract_title_from_html(html_content)

    # Try to extract publish date from Medium's metadata
    # Medium exports often have date in various formats
    time_tag = soup.find('time')
    if time_tag:
        datetime_attr = time_tag.get('datetime')
        if datetime_attr:
            try:
                # Parse ISO format date
                date_obj = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                metadata['date'] = date_obj.date().isoformat()
            except:
                pass

    # Try to extract tags/topics
    # Medium uses various classes for tags
    tags = []
    for tag_elem in soup.find_all(['a', 'span'], class_=re.compile(r'tag|topic', re.I)):
        tag_text = tag_elem.get_text().strip()
        if tag_text and len(tag_text) < 50:  # Reasonable tag length
            tags.append(tag_text)

    if tags:
        metadata['tags'] = list(set(tags))  # Remove duplicates

    # Try to extract featured image
    img_tags = soup.find_all('img')
    if img_tags:
        # Get first significant image (not icons/avatars)
        for img in img_tags:
            src = img.get('src', '')
            if src and ('cdn-images' in src or 'medium.com' in src):
                # Likely a content image, not an icon
                if 'max/800' in src or 'max/1024' in src or 'max/2000' in src:
                    metadata['thumbnail'] = src
                    break

    return metadata


def interactive_prompt_metadata(html_path: Path, extracted_meta: dict) -> dict:
    """
    Interactively prompt user for missing metadata.

    Args:
        html_path: Path to HTML file (for defaults)
        extracted_meta: Already extracted metadata

    Returns:
        Complete metadata dictionary
    """
    print("\n" + "="*60)
    print("📝 Blog Post Metadata")
    print("="*60)

    metadata = {}

    # Title
    default_title = extracted_meta.get('title', html_path.stem.replace('_', ' ').replace('-', ' '))
    title = input(f"Title [{default_title}]: ").strip()
    metadata['title'] = title if title else default_title

    # Slug
    default_slug = slugify(metadata['title'])
    slug = input(f"Slug (URL-friendly) [{default_slug}]: ").strip()
    metadata['slug'] = slug if slug else default_slug

    # Date
    default_date = extracted_meta.get('date', datetime.now().date().isoformat())
    date = input(f"Published Date (YYYY-MM-DD) [{default_date}]: ").strip()
    metadata['date'] = date if date else default_date

    # Tags
    default_tags = ', '.join(extracted_meta.get('tags', []))
    tags_input = input(f"Tags (comma-separated) [{default_tags}]: ").strip()
    if tags_input:
        metadata['tags'] = [tag.strip() for tag in tags_input.split(',')]
    elif default_tags:
        metadata['tags'] = extracted_meta.get('tags', [])
    else:
        metadata['tags'] = []

    # Thumbnail
    default_thumbnail = extracted_meta.get('thumbnail', '')
    thumbnail = input(f"Thumbnail URL [{default_thumbnail}]: ").strip()
    metadata['thumbnail'] = thumbnail if thumbnail else default_thumbnail

    # Status
    status = input("Status (published/draft) [published]: ").strip().lower()
    metadata['status'] = status if status in ['published', 'draft', 'archived'] else 'published'

    return metadata


def import_medium_post(
    html_path: Path,
    title: Optional[str] = None,
    slug: Optional[str] = None,
    date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    thumbnail: Optional[str] = None,
    status: str = 'published',
    dry_run: bool = False,
    interactive: bool = True
) -> bool:
    """
    Import a Medium post from HTML file to DynamoDB.

    Args:
        html_path: Path to HTML file
        title: Post title (optional, will be extracted or prompted)
        slug: URL slug (optional, will be generated or prompted)
        date: Published date (optional, will be extracted or prompted)
        tags: List of tags (optional, will be extracted or prompted)
        thumbnail: Thumbnail URL (optional, will be extracted or prompted)
        status: Post status (published/draft/archived)
        dry_run: If True, don't actually write to DynamoDB
        interactive: If True, prompt for missing metadata

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read HTML file
        if not html_path.exists():
            print(f"❌ File not found: {html_path}")
            return False

        print(f"📖 Reading HTML file: {html_path.name}")
        html_content = html_path.read_text(encoding='utf-8')

        # Extract metadata from HTML
        print("🔍 Extracting metadata from HTML...")
        extracted_meta = extract_medium_metadata(html_content)

        # Build metadata dict
        if interactive and not all([title, slug, date]):
            # Interactive mode - prompt for missing fields
            metadata = interactive_prompt_metadata(html_path, extracted_meta)
        else:
            # Non-interactive mode - use provided or extracted values
            metadata = {
                'title': title or extracted_meta.get('title', html_path.stem),
                'slug': slug or slugify(title or extracted_meta.get('title', html_path.stem)),
                'date': date or extracted_meta.get('date', datetime.now().date().isoformat()),
                'tags': tags or extracted_meta.get('tags', []),
                'thumbnail': thumbnail or extracted_meta.get('thumbnail', ''),
                'status': status
            }

        # Extract text content for AI
        print("📄 Extracting text content...")
        text_content = extract_text_from_html(html_content)

        # Generate excerpt
        excerpt = extract_excerpt_from_text(text_content, max_length=200)

        # Create BlogPost object
        blog_post = BlogPost(
            postId=metadata['slug'],
            title=metadata['title'],
            html_content=html_content,
            text_content=text_content,
            excerpt=excerpt,
            published_date=metadata['date'],
            created_date=metadata['date'],
            status=metadata['status'],
            tags=metadata['tags'],
            thumbnail=metadata['thumbnail'],
            view_count=0
        )

        # Display summary
        print("\n" + "="*60)
        print("📋 Post Summary")
        print("="*60)
        print(f"Title:     {blog_post.title}")
        print(f"Post ID:   {blog_post.postId}")
        print(f"Date:      {blog_post.published_date}")
        print(f"Status:    {blog_post.status}")
        print(f"Tags:      {', '.join(blog_post.tags) if blog_post.tags else '(none)'}")
        print(f"Thumbnail: {blog_post.thumbnail if blog_post.thumbnail else '(none)'}")
        print(f"HTML size: {len(blog_post.html_content):,} chars")
        print(f"Text size: {len(blog_post.text_content):,} chars")
        print(f"Excerpt:   {blog_post.excerpt[:80]}..." if len(blog_post.excerpt) > 80 else f"Excerpt:   {blog_post.excerpt}")
        print("="*60)

        if dry_run:
            print("\n🔍 DRY RUN - Post would be saved to DynamoDB")
            return True

        # Confirm before saving (if interactive)
        if interactive:
            confirm = input("\n✅ Save this post to DynamoDB? (y/n) [y]: ").strip().lower()
            if confirm and confirm != 'y':
                print("❌ Import cancelled")
                return False

        # Save to DynamoDB
        print("\n💾 Saving to DynamoDB...")
        item = blog_post.model_dump(by_alias=True)
        # Add slug field (same as postId) for compatibility with BlogPostSummary
        item['slug'] = blog_post.postId
        success = blog_db.put_item(item)

        if success:
            print(f"✅ Successfully imported post: {blog_post.title}")
            print(f"   Post ID: {blog_post.postId}")
            print(f"   URL: /blog/{blog_post.postId}")
            return True
        else:
            print(f"❌ Failed to save post to DynamoDB")
            return False

    except Exception as e:
        print(f"❌ Error importing post: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Import Medium blog post HTML to DynamoDB',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('html_file', type=Path, help='Path to Medium HTML export file')
    parser.add_argument('--title', type=str, help='Post title (will be extracted if not provided)')
    parser.add_argument('--slug', type=str, help='URL slug (will be generated if not provided)')
    parser.add_argument('--date', type=str, help='Published date (YYYY-MM-DD, will use today if not provided)')
    parser.add_argument('--tags', type=str, help='Comma-separated tags')
    parser.add_argument('--thumbnail', type=str, help='Thumbnail image URL')
    parser.add_argument('--status', type=str, choices=['published', 'draft', 'archived'],
                        default='published', help='Post status (default: published)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving to DynamoDB')
    parser.add_argument('--local', action='store_true', help='Use local DynamoDB instance')
    parser.add_argument('--non-interactive', action='store_true', help='Non-interactive mode (no prompts)')

    args = parser.parse_args()

    # Set environment for local DynamoDB if requested
    if args.local:
        os.environ['IS_LOCAL'] = 'true'
        os.environ['STAGE'] = 'local'
        print("🔧 Using local DynamoDB at http://localhost:8002\n")

    # Parse tags if provided
    tags_list = None
    if args.tags:
        tags_list = [tag.strip() for tag in args.tags.split(',')]

    # Import the post
    success = import_medium_post(
        html_path=args.html_file,
        title=args.title,
        slug=args.slug,
        date=args.date,
        tags=tags_list,
        thumbnail=args.thumbnail,
        status=args.status,
        dry_run=args.dry_run,
        interactive=not args.non_interactive
    )

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
