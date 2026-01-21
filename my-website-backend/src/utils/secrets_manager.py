"""
AWS Secrets Manager client with caching.
"""

import boto3
from botocore.exceptions import ClientError
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import threading


class SecretsManager:
    """
    AWS Secrets Manager client with thread-safe caching.
    Caches secrets for 5 minutes to reduce AWS API calls and improve performance.
    """

    def __init__(self, region_name: Optional[str] = None):
        """
        Initialize Secrets Manager client.

        Args:
            region_name: AWS region name (defaults to environment variable or ap-southeast-2)
        """
        self.region_name = region_name or os.getenv('AWS_REGION', 'ap-southeast-2')
        self.client = boto3.client('secretsmanager', region_name=self.region_name)
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_ttl_seconds = 300  # 5 minutes
        self._lock = threading.Lock()

    def get_secret(self, secret_name: str, force_refresh: bool = False) -> Optional[str]:
        """
        Retrieve a secret from AWS Secrets Manager with caching.

        Args:
            secret_name: Name of the secret in AWS Secrets Manager
            force_refresh: Force refresh from AWS (bypass cache)

        Returns:
            Secret value as string, or None if not found/error
        """
        # Check cache first (unless force refresh)
        if not force_refresh:
            cached_value = self._get_from_cache(secret_name)
            if cached_value is not None:
                return cached_value

        # Fetch from AWS Secrets Manager
        try:
            response = self.client.get_secret_value(SecretId=secret_name)

            # Parse secret value
            if 'SecretString' in response:
                secret_value = response['SecretString']
            else:
                # Binary secrets are base64 encoded
                secret_value = response['SecretBinary'].decode('utf-8')

            # Update cache
            self._update_cache(secret_name, secret_value)

            return secret_value

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                print(f"Secret '{secret_name}' not found in AWS Secrets Manager")
            elif error_code == 'InvalidRequestException':
                print(f"Invalid request for secret '{secret_name}': {str(e)}")
            elif error_code == 'InvalidParameterException':
                print(f"Invalid parameter for secret '{secret_name}': {str(e)}")
            elif error_code == 'DecryptionFailure':
                print(f"Failed to decrypt secret '{secret_name}': {str(e)}")
            elif error_code == 'InternalServiceError':
                print(f"AWS Secrets Manager internal error for secret '{secret_name}': {str(e)}")
            else:
                print(f"Error retrieving secret '{secret_name}': {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error retrieving secret '{secret_name}': {str(e)}")
            return None

    def get_secret_json(self, secret_name: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        Retrieve a JSON secret from AWS Secrets Manager.

        Args:
            secret_name: Name of the secret in AWS Secrets Manager
            force_refresh: Force refresh from AWS (bypass cache)

        Returns:
            Secret value as dictionary, or None if not found/error
        """
        secret_string = self.get_secret(secret_name, force_refresh)
        if secret_string is None:
            return None

        try:
            return json.loads(secret_string)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON secret '{secret_name}': {str(e)}")
            return None

    def _get_from_cache(self, secret_name: str) -> Optional[str]:
        """
        Get secret from cache if not expired.

        Args:
            secret_name: Name of the secret

        Returns:
            Cached secret value or None if expired/not found
        """
        with self._lock:
            if secret_name in self.cache:
                cached_item = self.cache[secret_name]
                expiry_time = cached_item['expiry']

                if datetime.now() < expiry_time:
                    return cached_item['value']
                else:
                    # Remove expired cache entry
                    del self.cache[secret_name]

        return None

    def _update_cache(self, secret_name: str, value: str) -> None:
        """
        Update cache with new secret value.

        Args:
            secret_name: Name of the secret
            value: Secret value to cache
        """
        with self._lock:
            self.cache[secret_name] = {
                'value': value,
                'expiry': datetime.now() + timedelta(seconds=self.cache_ttl_seconds)
            }

    def clear_cache(self, secret_name: Optional[str] = None) -> None:
        """
        Clear cache for a specific secret or all secrets.

        Args:
            secret_name: Name of the secret to clear (or None for all secrets)
        """
        with self._lock:
            if secret_name:
                self.cache.pop(secret_name, None)
            else:
                self.cache.clear()

    def get_api_key(self, provider: str, stage: Optional[str] = None) -> Optional[str]:
        """
        Convenience method to get API keys for AI providers.

        Args:
            provider: Provider name (openai, anthropic, gemini)
            stage: Deployment stage (defaults to environment variable)

        Returns:
            API key string or None
        """
        stage = stage or os.getenv('STAGE', 'dev')
        secret_name = f"{stage}/portfolio/{provider}-api-key"
        return self.get_secret(secret_name)


# Global instance for reuse
secrets_manager = SecretsManager()
