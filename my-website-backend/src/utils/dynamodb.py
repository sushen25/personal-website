"""
DynamoDB utilities - imported from shared portfolio-common package.
"""

import os
from portfolio_common.utils.dynamodb import DynamoDBHelper, IS_LOCAL, AWS_REGION
from boto3.dynamodb.conditions import Key, Attr

# Service-specific table configuration
CHAT_TABLE = os.getenv('CHAT_CONVERSATIONS_TABLE', 'dev-portfolio-chat-conversations')
BLOG_TABLE = os.getenv('BLOG_POSTS_TABLE', 'dev-portfolio-blog-posts')
ANALYTICS_TABLE = os.getenv('ANALYTICS_TABLE', 'dev-portfolio-analytics')

# Service-specific pre-initialized helper instances for each table
chat_db = DynamoDBHelper(CHAT_TABLE)
blog_db = DynamoDBHelper(BLOG_TABLE)
analytics_db = DynamoDBHelper(ANALYTICS_TABLE)

__all__ = ['DynamoDBHelper', 'chat_db', 'blog_db', 'analytics_db', 'Key', 'Attr', 'IS_LOCAL', 'AWS_REGION']
