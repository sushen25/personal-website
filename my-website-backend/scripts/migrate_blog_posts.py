#!/usr/bin/env python3
"""
Migrate blog posts from frontend static files to DynamoDB.

This script:
1. Reads posts metadata from the frontend posts.ts file
2. Reads HTML content from the articles directory
3. Extracts text content for AI consumption
4. Saves everything to DynamoDB

Usage:
    python scripts/migrate_blog_posts.py [--dry-run] [--local]

Options:
    --dry-run: Show what would be migrated without actually writing to DynamoDB
    --local: Use local DynamoDB instance (http://localhost:8002)
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime
import argparse

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.text_extractor import extract_text_from_html, extract_excerpt_from_text
from src.utils.dynamodb import blog_db, dynamodb_resource, BLOG_TABLE
from src.models.schemas import BlogPost


def parse_posts_ts(frontend_path: Path) -> list:
    """
    Parse the posts.ts file to extract post metadata.

    Args:
        frontend_path: Path to the frontend directory

    Returns:
        List of post dictionaries
    """
    posts_file = frontend_path / "src/app/blog/posts.ts"

    if not posts_file.exists():
        print(f"❌ Posts file not found: {posts_file}")
        return []


    content = posts_file.read_text()



    # Extract the posts array using regex
    # This is a simple parser - assumes the posts.ts structure is consistent
    # Format: export const posts = [...]
    match = re.search(r'export const posts = \[(.*?)\]', content, re.DOTALL)

    if not match:
        print("❌ Could not find posts array in posts.ts")
        return []

    posts_str = match.group(1)

    print("Posts string: ", posts_str)

    # Parse each post object (simplified - assumes consistent formatting)
    post_pattern = r'\{([^}]+)\}'
    posts = []

    for match in re.finditer(post_pattern, posts_str):
        post_obj = match.group(1)

        # Extract fields
        post = {}
        field_pattern = r'(\w+):\s*(["\[].*?["\]])'

        for field_match in re.finditer(field_pattern, post_obj):
            field_name = field_match.group(1)
            field_value = field_match.group(2)

            # Clean up the value
            if field_value.startswith('"') and field_value.endswith('"'):
                # String value
                post[field_name] = field_value[1:-1]
            elif field_value.startswith('['):
                # Array value - extract strings from array
                array_items = re.findall(r'"([^"]+)"', field_value)
                post[field_name] = array_items
            else:
                post[field_name] = field_value

        if post:
            posts.append(post)

    return posts


def read_html_article(frontend_path: Path, article_filename: str) -> str:
    """
    Read HTML content from an article file.

    Args:
        frontend_path: Path to the frontend directory
        article_filename: Article filename

    Returns:
        HTML content as string
    """
    article_path = frontend_path / "src/app/blog/articles" / article_filename

    if not article_path.exists():
        print(f"⚠️  Article file not found: {article_path}")
        return ""

    return article_path.read_text()


def migrate_post(post_meta: dict, frontend_path: Path, dry_run: bool = False) -> bool:
    """
    Migrate a single blog post to DynamoDB.

    Args:
        post_meta: Post metadata from posts.ts
        frontend_path: Path to frontend directory
        dry_run: If True, don't actually write to DynamoDB

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read HTML content
        html_content = read_html_article(frontend_path, post_meta.get('article', ''))

        if not html_content:
            print(f"⚠️  Skipping {post_meta.get('slug')} - no HTML content")
            return False

        # Extract text content for AI
        text_content = extract_text_from_html(html_content)

        print("CONTENT")
        print(html_content)

        # Extract excerpt if not provided
        excerpt = post_meta.get('content', '')
        if not excerpt or len(excerpt) < 10:
            excerpt = extract_excerpt_from_text(text_content, max_length=200)

        # Create BlogPost object
        blog_post = BlogPost(
            postId=post_meta['slug'],
            slug=post_meta['slug'],
            title=post_meta['title'],
            html_content=html_content,
            text_content=text_content,
            excerpt=excerpt,
            published_date=post_meta.get('date', datetime.now().date().isoformat()),
            created_date=post_meta.get('date', datetime.now().date().isoformat()),
            status="published",
            tags=post_meta.get('tags', []),
            thumbnail=post_meta.get('thumbnail'),
            view_count=0
        )

        if dry_run:
            print(f"  [DRY RUN] Would migrate: {blog_post.title}")
            print(f"    Slug: {blog_post.slug}")
            print(f"    Date: {blog_post.published_date}")
            print(f"    Tags: {', '.join(blog_post.tags)}")
            print(f"    HTML length: {len(blog_post.html_content)} chars")
            print(f"    Text length: {len(blog_post.text_content)} chars")
            return True

        # Save to DynamoDB (use aliases to get camelCase field names)
        item = blog_post.model_dump(by_alias=True)
        success = blog_db.put_item(item)

        if success:
            print(f"  ✅ Migrated: {blog_post.title}")
            return True
        else:
            print(f"  ❌ Failed to migrate: {blog_post.title}")
            return False

    except Exception as e:
        print(f"  ❌ Error migrating post: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main migration script."""
    parser = argparse.ArgumentParser(description='Migrate blog posts to DynamoDB')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be migrated without writing')
    parser.add_argument('--local', action='store_true', help='Use local DynamoDB (implies setting IS_LOCAL=true)')
    args = parser.parse_args()

    # Set environment for local DynamoDB if requested
    if args.local:
        os.environ['IS_LOCAL'] = 'true'
        os.environ['STAGE'] = 'local'
        print("🔧 Using local DynamoDB")

    print("=" * 60)
    print("Blog Posts Migration to DynamoDB")
    print("=" * 60)

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")

    # Locate frontend directory
    script_dir = Path(__file__).parent
    backend_dir = script_dir.parent
    repo_root = backend_dir.parent
    frontend_path = repo_root / "my-website-frontend"

    if not frontend_path.exists():
        print(f"❌ Frontend directory not found: {frontend_path}")
        return 1

    print(f"\n📂 Frontend path: {frontend_path}")
    print(f"📊 DynamoDB table: {BLOG_TABLE}\n")

    # Parse posts from frontend
    print("📖 Reading posts from frontend...")


    

    # Migrate each post
    success_count = 0
    failed_count = 0

    posts = [
        {
            "title": "Standardising AI Access - Model Context Protocol (MCP)",
            "slug": "standardising-ai-access-model-context-protocol-mcp",
            "date": "2025-10-09",
            "content": "Standardising AI Access - Model Context Protocol (MCP)",
            "article": "2025-10-09_Standardising_AI_Access_-_Model_Context_Protocol.html",
            "tags": ["AI", "MCP", "Model Context Protocol", "Standardising AI Access"],
            "thumbnail": "https://cdn-images-1.medium.com/max/800/1*rFxZfu8pJzpGTIY8e9F97w.png"
        }
    ]

    print(f"Found {len(posts)} post(s) to migrate\n")

    for post in posts:
        print(f"Processing: {post.get('title', 'Unknown')}")
        if migrate_post(post, frontend_path, dry_run=args.dry_run):
            success_count += 1
        else:
            failed_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("Migration Summary")
    print("=" * 60)
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total: {len(posts)}")

    if args.dry_run:
        print("\n💡 This was a dry run. Run without --dry-run to actually migrate.")

    return 0 if failed_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
