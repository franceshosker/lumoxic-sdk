"""Custom exceptions for the Lumoxic SDK."""

from __future__ import annotations

from typing import Any


class LumoxicError(Exception):
    """Base exception for all Lumoxic SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body or {}

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(LumoxicError):
    """Raised when the API key is missing, invalid, or expired."""

    def __init__(
        self,
        message: str = "Authentication failed. Check your API key.",
        status_code: int = 401,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code, response_body)


class RateLimitError(LumoxicError):
    """Raised when the API rate limit has been exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded. Please wait before retrying.",
        status_code: int = 429,
        response_body: dict[str, Any] | None = None,
        retry_after: float | None = None,
    ) -> None:
        super().__init__(message, status_code, response_body)
        self.retry_after = retry_after


class ValidationError(LumoxicError):
    """Raised when request parameters fail server-side validation."""

    def __init__(
        self,
        message: str = "Request validation failed.",
        status_code: int = 422,
        response_body: dict[str, Any] | None = None,
        field_errors: dict[str, list[str]] | None = None,
    ) -> None:
        super().__init__(message, status_code, response_body)
        self.field_errors = field_errors or {}


class ServerError(LumoxicError):
    """Raised when the Lumoxic API returns a 5xx server error."""

    def __init__(
        self,
        message: str = "Internal server error. Please try again later.",
        status_code: int = 500,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code, response_body)


class TimeoutError(LumoxicError):
    """Raised when a request to the Lumoxic API times out."""

    def __init__(
        self,
        message: str = "Request timed out.",
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code, response_body)


class NotFoundError(LumoxicError):
    """Raised when the requested resource does not exist."""

    def __init__(
        self,
        message: str = "Resource not found.",
        status_code: int = 404,
        response_body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code, response_body)
