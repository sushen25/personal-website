"""
AWS Secrets Manager client with caching for API keys.
"""

import boto3
import os
import json
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
import threading


class SecretsManager:
    """
    Thread-safe Secrets Manager client with caching.
    
    Caches secrets for 5 minutes to reduce API calls and improve performance.
    """

    def __init__(self, cache_ttl_minutes: int = 5):
        """
        Initialize Secrets Manager.

        Args:
            cache_ttl_minutes: Cache TTL in minutes (default: 5)
        """
        self.client = boto3.client(
            'secretsmanager',
            region_name=os.getenv('AWS_REGION', 'ap-southeast-2')
        )
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        self._cache: Dict[str, Tuple[str, datetime]] = {}
        self._lock = threading.Lock()

    def get_secret(self, secret_name: str) -> str:
        """
        Get secret value from AWS Secrets Manager (with caching).

        Args:
            secret_name: Name of the secret (e.g., "dev/portfolio/openai-api-key")

        Returns:
            Secret value as string

        Raises:
            Exception: If secret cannot be retrieved
        """
        # Check cache first
        with self._lock:
            if secret_name in self._cache:
                secret_value, cached_time = self._cache[secret_name]
                if datetime.now() - cached_time < self.cache_ttl:
                    return secret_value
                # Cache expired, remove it
                del self._cache[secret_name]

        # Fetch from AWS
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            secret_value = response['SecretString']
            
            # Try to parse as JSON (some secrets are stored as JSON)
            try:
                secret_dict = json.loads(secret_value)
                # If it's a dict, try to get common key names
                if isinstance(secret_dict, dict):
                    secret_value = secret_dict.get('api_key') or secret_dict.get('API_KEY') or secret_dict.get('value') or secret_value
            except (json.JSONDecodeError, AttributeError):
                pass  # Not JSON, use as-is

            # Cache the value
            with self._lock:
                self._cache[secret_name] = (secret_value, datetime.now())

            return secret_value

        except Exception as e:
            raise Exception(f"Failed to retrieve secret '{secret_name}': {str(e)}")

    def clear_cache(self):
        """Clear the cache (useful for testing or forced refresh)."""
        with self._lock:
            self._cache.clear()

