# Portfolio Common

Shared utilities, models, and services for the portfolio website.

## Overview

This package provides common code shared between:
- `my-website-backend` (FastAPI backend API)
- `agent-service` (Strands Agents AI service)

## Installation

Install in editable mode from the parent project:

```bash
pip install -e ../portfolio-common
```

## Modules

### `portfolio_common.utils`
- `dynamodb.py` - DynamoDB client wrapper and utilities
- `text_extractor.py` - HTML to text conversion and excerpt generation

### `portfolio_common.models`
- `schemas.py` - Pydantic data models (BlogPost, ChatMessage, etc.)

### `portfolio_common.services`
- `blog_service.py` - Blog post CRUD operations

### `portfolio_common.exceptions`
- Custom exception classes for error handling

## Development

The package uses Python 3.11 and follows modern Python packaging conventions with `pyproject.toml`.

## Dependencies

Core dependencies:
- boto3 - AWS SDK for DynamoDB
- pydantic - Data validation
- beautifulsoup4 - HTML processing
- python-dotenv - Environment variable management
