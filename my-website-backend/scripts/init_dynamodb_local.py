#!/usr/bin/env python3
"""
Initialize local DynamoDB tables for development.
Run this after starting the local DynamoDB instance with docker-compose.
"""

import boto3
from botocore.exceptions import ClientError

# Configure DynamoDB client for local instance
dynamodb = boto3.client(
    'dynamodb',
    endpoint_url='http://localhost:8002',
    region_name='ap-southeast-2',
    aws_access_key_id='local',
    aws_secret_access_key='local'
)

def create_chat_conversations_table(stage='dev'):
    """Create the chat conversations table matching serverless.yml configuration."""
    table_name = f'{stage}-portfolio-chat-conversations'

    try:
        # Check if table already exists
        existing_tables = dynamodb.list_tables()['TableNames']
        if table_name in existing_tables:
            print(f"✓ Table {table_name} already exists")
            return

        # Create table with same schema as serverless.yml
        response = dynamodb.create_table(
            TableName=table_name,
            BillingMode='PAY_PER_REQUEST',
            AttributeDefinitions=[
                {'AttributeName': 'sessionId', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'N'},
                {'AttributeName': 'createdDate', 'AttributeType': 'S'},
            ],
            KeySchema=[
                {'AttributeName': 'sessionId', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'},
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'CreatedDateIndex',
                    'KeySchema': [
                        {'AttributeName': 'createdDate', 'KeyType': 'HASH'},
                        {'AttributeName': 'timestamp', 'KeyType': 'RANGE'},
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            StreamSpecification={
                'StreamEnabled': True,
                'StreamViewType': 'NEW_AND_OLD_IMAGES'
            }
        )

        print(f"✓ Created table: {table_name}")
        print(f"  - Primary key: sessionId (HASH) + timestamp (RANGE)")
        print(f"  - GSI: CreatedDateIndex")
        print(f"  - Streams: Enabled")

    except ClientError as e:
        print(f"✗ Error creating table {table_name}: {e}")
        raise

def list_tables():
    """List all tables in the local DynamoDB instance."""
    try:
        response = dynamodb.list_tables()
        tables = response['TableNames']
        print(f"\nTables in local DynamoDB:")
        if tables:
            for table in tables:
                print(f"  - {table}")
        else:
            print("  (none)")
    except ClientError as e:
        print(f"✗ Error listing tables: {e}")

def main():
    print("Initializing local DynamoDB tables...")
    print(f"Connecting to: http://localhost:8002\n")

    # Create tables
    create_chat_conversations_table(stage='dev')

    # List all tables
    list_tables()

    print("\n✓ Local DynamoDB initialization complete!")
    print("\nYou can now use the local DynamoDB instance at:")
    print("  Endpoint: http://localhost:8002")
    print("  Region: ap-southeast-2")
    print("  AWS Access Key: local")
    print("  AWS Secret Key: local")

if __name__ == '__main__':
    main()
