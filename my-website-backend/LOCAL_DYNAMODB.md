# Local DynamoDB Setup

This guide explains how to set up and use a local DynamoDB instance for development and testing.

## Prerequisites

- Docker installed and running
- Python 3.11+ with boto3 installed

## Quick Start

### 1. Start Local DynamoDB

Start the local DynamoDB instance using Docker Compose:

```bash
docker-compose up -d
```

This will:
- Start DynamoDB Local on port 8001 (mapped from container port 8000)
- Create a persistent volume in `./dynamodb-data` for storing data
- Use local credentials (access key: `local`, secret key: `local`)

### 2. Initialize Tables

Run the initialization script to create the tables:

```bash
python scripts/init_dynamodb_local.py
```

This will create:
- `dev-portfolio-chat-conversations` table with the schema from `serverless.yml`

### 3. Verify Setup

Check that DynamoDB is running and tables are created:

```bash
# List tables
aws dynamodb list-tables \
  --endpoint-url http://localhost:8001 \
  --region ap-southeast-2

# Describe a specific table
aws dynamodb describe-table \
  --table-name dev-portfolio-chat-conversations \
  --endpoint-url http://localhost:8001 \
  --region ap-southeast-2
```

## Using Local DynamoDB in Your Application

### Environment Variables

The application automatically detects local mode and uses the local DynamoDB endpoint when either:
- `STAGE=local` is set, OR
- `IS_LOCAL=true` is set

**Option 1: Update your `.env` file:**

```bash
# Set either of these:
STAGE=local
# OR
IS_LOCAL=true
```

**Option 2: Set environment variables in your shell:**

```bash
export STAGE=local
# OR
export IS_LOCAL=true
```

The application will automatically:
- Connect to `http://localhost:8002` for DynamoDB
- Use local credentials (access key: `local`, secret key: `local`)
- Print `🔧 Using local DynamoDB at http://localhost:8002` on startup

### Python Code Example

```python
import boto3

# For local development
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8001',
    region_name='ap-southeast-2',
    aws_access_key_id='local',
    aws_secret_access_key='local'
)

# Access table
table = dynamodb.Table('dev-portfolio-chat-conversations')
```

## DynamoDB Admin UI (Optional)

You can use a GUI tool to browse and manage local DynamoDB tables:

### Option 1: dynamodb-admin (npm)

```bash
# Install globally
npm install -g dynamodb-admin

# Run with local endpoint on port 8003
DYNAMO_ENDPOINT=http://localhost:8002 dynamodb-admin --port 8003
```

Then open http://localhost:8003 in your browser to access the DynamoDB admin UI.

### Option 2: NoSQL Workbench

Download AWS NoSQL Workbench from AWS website and configure it to connect to `http://localhost:8001`.

## Managing the Local Instance

### Stop DynamoDB

```bash
docker-compose down
```

### Clear All Data

```bash
# Stop and remove containers and volumes
docker-compose down -v

# Remove data directory
rm -rf dynamodb-data/

# Restart and reinitialize
docker-compose up -d
python scripts/init_dynamodb_local.py
```

### View Logs

```bash
docker-compose logs -f dynamodb-local
```

## Table Schema

### Chat Conversations Table

- **Table Name**: `dev-portfolio-chat-conversations`
- **Primary Key**:
  - `sessionId` (String) - Hash key
  - `timestamp` (Number) - Range key
- **Global Secondary Index**:
  - `CreatedDateIndex`: `createdDate` (Hash) + `timestamp` (Range)
- **Features**:
  - TTL enabled on `ttl` attribute
  - DynamoDB Streams enabled

## Troubleshooting

### Port already in use

The default configuration uses port 8001. If this port is already in use, you can change it in `docker-compose.yml`:

```yaml
ports:
  - "8002:8000"  # Use 8002 instead
```

Then update the endpoint URL in `scripts/init_dynamodb_local.py` and your application code.

### Table already exists error

The initialization script checks if tables exist before creating them. If you get errors, try:

```bash
# Stop DynamoDB
docker-compose down

# Clear data
rm -rf dynamodb-data/

# Start fresh
docker-compose up -d
python scripts/init_dynamodb_local.py
```

### Connection refused

Make sure DynamoDB is running:

```bash
docker-compose ps
```

You should see `portfolio-dynamodb-local` with status "Up".
