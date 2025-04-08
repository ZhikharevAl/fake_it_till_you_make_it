from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class AuthPayload(BaseModel):
    """Request body model for POST /api/auth (login data)."""

    login: EmailStr | str = Field(..., min_length=1, description="User Login")
    password: str = Field(..., min_length=1, description="User password")


class AuthSuccessResponse(BaseModel):
    """Successful response model for POST /api/auth (200 OK)."""

    auth: Literal[True]
    token: str = Field(..., min_length=10, description="JWT access token")

    @field_validator("auth")
    @classmethod
    def check_auth_is_true(cls, auth_value: Literal[True]) -> Literal[True]:
        """Checks that the 'auth' flag is True on success."""
        if auth_value is not True:
            raise ValueError(
                "The 'auth' field should be true on successful authorization"
            )  # For the custom message
        return auth_value
