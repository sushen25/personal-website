"""
Blog service for managing blog posts and interactions.
"""

from typing import List, Optional, Dict, Any
from boto3.dynamodb.conditions import Key
from datetime import datetime

from portfolio_common.models.schemas import BlogPost, BlogPostSummary
from portfolio_common.utils.text_extractor import extract_text_from_html, extract_excerpt_from_text
from portfolio_common.exceptions import NotFoundError, ValidationError


class BlogService:
    """Service for managing blog post operations."""

    def __init__(self, blog_db):
        """
        Initialize blog service with DynamoDB helper.

        Args:
            blog_db: DynamoDBHelper instance for blog posts table
        """
        self.blog_db = blog_db

    async def create_post(self, post: BlogPost) -> BlogPost:
        """
        Create a new blog post.

        Automatically extracts text content from HTML if not provided.
        Sets created_date if not provided.

        Args:
            post: BlogPost object to create

        Returns:
            Created BlogPost with all fields populated

        Raises:
            ValidationError: If post data is invalid
        """
        try:
            # Ensure postId and slug are the same
            if post.postId != post.slug:
                raise ValidationError(
                    message="postId must equal slug",
                    detail={"postId": post.postId, "slug": post.slug}
                )

            # Auto-extract text_content if not provided or empty
            if not post.text_content or post.text_content.strip() == "":
                post.text_content = extract_text_from_html(post.html_content)

            # Auto-generate excerpt if not provided
            if not post.excerpt:
                post.excerpt = extract_excerpt_from_text(post.text_content, max_length=200)

            # Set created_date if not provided
            if not post.created_date:
                post.created_date = datetime.now().date().isoformat()

            # Convert to dict for DynamoDB (use aliases for camelCase field names)
            item = post.model_dump(by_alias=True)

            # Save to DynamoDB
            self.blog_db.put_item(item)

            return post

        except ValidationError:
            raise
        except Exception as e:
            print(f"Error creating blog post: {str(e)}")
            raise Exception(f"Failed to create blog post: {str(e)}")

    async def get_post_by_slug(self, slug: str) -> BlogPost:
        """
        Get a blog post by slug.

        Args:
            slug: Post slug (URL-friendly identifier)

        Returns:
            BlogPost object

        Raises:
            NotFoundError: If post not found
        """
        try:
            # Query by primary key (postId = slug)
            item = self.blog_db.get_item({'postId': slug})

            if not item:
                raise NotFoundError(
                    message=f"Blog post not found: {slug}",
                    detail={"slug": slug}
                )

            # Convert to BlogPost model
            return BlogPost(**item)

        except NotFoundError:
            raise
        except Exception as e:
            print(f"Error retrieving blog post: {str(e)}")
            raise Exception(f"Failed to retrieve blog post: {str(e)}")

    async def list_posts(
        self,
        status: str = "published",
        limit: int = 100
    ) -> List[BlogPostSummary]:
        """
        List blog posts filtered by status, sorted by creation date (newest first).

        Args:
            status: Post status filter (published, draft, archived)
            limit: Maximum number of posts to return

        Returns:
            List of BlogPostSummary objects
        """
        try:
            # Query using StatusCreatedDateIndex GSI
            items = self.blog_db.scan()

            summaries = []
            for item in items:
                try:
                    summaries.append(BlogPostSummary(**item))
                except Exception as e:
                    print(f"Error converting item to BlogPostSummary: {e}")
                    print(f"Item: {item}")
                    continue
            

            return summaries

        except Exception as e:
            print(f"Error listing blog posts: {str(e)}")
            raise Exception(f"Failed to list blog posts: {str(e)}")

    async def update_post(self, slug: str, updates: Dict[str, Any]) -> BlogPost:
        """
        Update a blog post.

        If html_content is updated, automatically re-extracts text_content.

        Args:
            slug: Post slug to update
            updates: Dictionary of fields to update

        Returns:
            Updated BlogPost object

        Raises:
            NotFoundError: If post not found
            ValidationError: If update data is invalid
        """
        try:
            # First, check if post exists
            existing = await self.get_post_by_slug(slug)

            # If html_content is being updated, re-extract text_content
            if 'html_content' in updates:
                updates['text_content'] = extract_text_from_html(updates['html_content'])

                # Re-generate excerpt if not explicitly provided
                if 'excerpt' not in updates:
                    updates['excerpt'] = extract_excerpt_from_text(
                        updates['text_content'],
                        max_length=200
                    )

            # Don't allow changing postId or slug
            updates.pop('postId', None)
            updates.pop('slug', None)

            # Build update expression
            update_expression = "SET " + ", ".join(
                f"#{k} = :{k}" for k in updates.keys()
            )

            expression_attribute_names = {
                f"#{k}": k for k in updates.keys()
            }

            expression_attribute_values = {
                f":{k}": v for k, v in updates.items()
            }

            # Update in DynamoDB
            self.blog_db.update_item(
                key={'postId': slug},
                update_expression=update_expression,
                expression_attribute_names=expression_attribute_names,
                expression_attribute_values=expression_attribute_values
            )

            # Return updated post
            return await self.get_post_by_slug(slug)

        except NotFoundError:
            raise
        except Exception as e:
            print(f"Error updating blog post: {str(e)}")
            raise Exception(f"Failed to update blog post: {str(e)}")

    async def delete_post(self, slug: str) -> bool:
        """
        Delete a blog post.

        Args:
            slug: Post slug to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            # Check if post exists first
            try:
                await self.get_post_by_slug(slug)
            except NotFoundError:
                return False

            # Delete from DynamoDB
            self.blog_db.delete_item({'postId': slug})
            return True

        except Exception as e:
            print(f"Error deleting blog post: {str(e)}")
            raise Exception(f"Failed to delete blog post: {str(e)}")

    async def increment_view_count(self, slug: str) -> int:
        """
        Increment the view count for a blog post.

        Args:
            slug: Post slug

        Returns:
            New view count

        Raises:
            NotFoundError: If post not found
        """
        try:
            # Increment view count atomically
            self.blog_db.update_item(
                key={'postId': slug},
                update_expression="SET view_count = if_not_exists(view_count, :zero) + :inc",
                expression_attribute_values={
                    ':inc': 1,
                    ':zero': 0
                }
            )

            # Get updated post to return new count
            post = await self.get_post_by_slug(slug)
            return post.view_count

        except NotFoundError:
            raise
        except Exception as e:
            print(f"Error incrementing view count: {str(e)}")
            raise Exception(f"Failed to increment view count: {str(e)}")
