"""
DynamoDB client and utility functions for agent service.
"""

import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Dict, List, Any, Optional
import os
from decimal import Decimal


# Detect local environment
IS_LOCAL = os.getenv('STAGE', 'dev') == 'local' or os.getenv('IS_LOCAL', 'false').lower() == 'true'
AWS_REGION = 'ap-southeast-2'

# Configure DynamoDB client and resource
if IS_LOCAL:
    # Local DynamoDB configuration
    dynamodb_client = boto3.client(
        'dynamodb',
        endpoint_url='http://localhost:8002',
        region_name=AWS_REGION,
        aws_access_key_id='local',
        aws_secret_access_key='local'
    )
    dynamodb_resource = boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:8002',
        region_name=AWS_REGION,
        aws_access_key_id='local',
        aws_secret_access_key='local'
    )
    print(f"🔧 Using local DynamoDB at http://localhost:8002")
else:
    # AWS DynamoDB configuration
    dynamodb_client = boto3.client('dynamodb', region_name=AWS_REGION)
    dynamodb_resource = boto3.resource('dynamodb', region_name=AWS_REGION)
    print(f"☁️  Using AWS DynamoDB in region {AWS_REGION}")

# Table names from environment variables
CHAT_TABLE = os.getenv('CHAT_CONVERSATIONS_TABLE', 'dev-portfolio-chat-conversations')
BLOG_TABLE = os.getenv('BLOG_POSTS_TABLE', 'dev-portfolio-blog-posts')
ANALYTICS_TABLE = os.getenv('ANALYTICS_TABLE', 'dev-portfolio-analytics')


class DynamoDBHelper:
    """Helper class for DynamoDB operations."""

    def __init__(self, table_name: str):
        """Initialize with table name."""
        self.table_name = table_name
        self.table = dynamodb_resource.Table(table_name)

    def get_item(self, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get a single item from DynamoDB.

        Args:
            key: Primary key dictionary (e.g., {'sessionId': 'abc', 'timestamp': 123})

        Returns:
            Item dictionary or None if not found
        """
        try:
            response = self.table.get_item(Key=key)
            return self._convert_decimal_to_float(response.get('Item'))
        except Exception as e:
            print(f"Error getting item from {self.table_name}: {str(e)}")
            return None

    def put_item(self, item: Dict[str, Any]) -> bool:
        """
        Put an item into DynamoDB.

        Args:
            item: Item dictionary to store

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert floats to Decimal for DynamoDB
            item = self._convert_floats_to_decimal(item)
            self.table.put_item(Item=item)
            return True
        except Exception as e:
            print(f"Error putting item to {self.table_name}: {str(e)}")
            return False

    def delete_item(self, key: Dict[str, Any]) -> bool:
        """
        Delete an item from DynamoDB.

        Args:
            key: Primary key dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            self.table.delete_item(Key=key)
            return True
        except Exception as e:
            print(f"Error deleting item from {self.table_name}: {str(e)}")
            return False

    def query(
        self,
        key_condition: Any,
        index_name: Optional[str] = None,
        filter_expression: Optional[Any] = None,
        limit: Optional[int] = None,
        scan_index_forward: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Query items from DynamoDB.

        Args:
            key_condition: Key condition expression
            index_name: Optional GSI name
            filter_expression: Optional filter expression
            limit: Optional limit on number of items
            scan_index_forward: Sort order (True=ascending, False=descending)

        Returns:
            List of items
        """
        try:
            query_params = {
                'KeyConditionExpression': key_condition,
                'ScanIndexForward': scan_index_forward
            }

            if index_name:
                query_params['IndexName'] = index_name

            if filter_expression:
                query_params['FilterExpression'] = filter_expression

            if limit:
                query_params['Limit'] = limit

            response = self.table.query(**query_params)
            items = response.get('Items', [])

            # Convert Decimal back to float
            return [self._convert_decimal_to_float(item) for item in items]
        except Exception as e:
            print(f"Error querying {self.table_name}: {str(e)}")
            return []

    def scan(
        self,
        filter_expression: Optional[Any] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan items from DynamoDB.

        Args:
            filter_expression: Optional filter expression
            limit: Optional limit on number of items

        Returns:
            List of items
        """
        try:
            scan_params = {}

            if filter_expression:
                scan_params['FilterExpression'] = filter_expression

            if limit:
                scan_params['Limit'] = limit

            response = self.table.scan(**scan_params)
            items = response.get('Items', [])

            return [self._convert_decimal_to_float(item) for item in items]
        except Exception as e:
            print(f"Error scanning {self.table_name}: {str(e)}")
            return []

    @staticmethod
    def _convert_floats_to_decimal(obj: Any) -> Any:
        """Convert floats to Decimal for DynamoDB compatibility."""
        if isinstance(obj, float):
            return Decimal(str(obj))
        elif isinstance(obj, dict):
            return {k: DynamoDBHelper._convert_floats_to_decimal(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [DynamoDBHelper._convert_floats_to_decimal(item) for item in obj]
        return obj

    @staticmethod
    def _convert_decimal_to_float(obj: Any) -> Any:
        """Convert Decimal to float for JSON serialization."""
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: DynamoDBHelper._convert_decimal_to_float(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [DynamoDBHelper._convert_decimal_to_float(item) for item in obj]
        return obj


# Pre-initialized helper instances for each table
chat_db = DynamoDBHelper(CHAT_TABLE)
blog_db = DynamoDBHelper(BLOG_TABLE)

