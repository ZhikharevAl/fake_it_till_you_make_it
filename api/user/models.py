import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class AddToFavouritesPayload(BaseModel):
    """Модель тела запроса для POST /api/user/favourites."""

    request_id: str = Field(
        ..., min_length=1, alias="requestId", description="ID запроса для добавления в избранное"
    )

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
    }


FavouritesListResponse = list[str]


class Location(BaseModel):
    """Модель местоположения."""

    latitude: float | None = None
    longitude: float | None = None
    district: str | None = None
    city: str | None = None
    model_config = {"populate_by_name": True, "extra": "ignore"}


class Education(BaseModel):
    """Модель образования."""

    organization_name: str | None = Field(None, alias="organizationName", examples=["МГУ"])
    level: Literal["Среднее общее", "Среднее профессиональное", "Высшее"] | None = None
    specialization: str | None = Field(None, examples=["Филология"])
    graduation_year: int | None = Field(None, alias="graduationYear", examples=[1980])
    model_config = {"populate_by_name": True, "extra": "ignore"}


class SocialContacts(BaseModel):
    """Модель контактов в соцсетях."""

    telegram: str | None = Field(None, examples=["@user"])
    whatsapp: str | None = Field(None, examples=["+123456789"])
    vk: str | None = Field(None, examples=["user_vk_id"])
    model_config = {"populate_by_name": True, "extra": "ignore"}


class Contacts(BaseModel):
    """Модель контактов пользователя."""

    email: EmailStr | None = Field(None, examples=["user@example.com"])
    phone: str | None = Field(None, examples=["+123456789"])
    social: SocialContacts | None = None
    model_config = {"populate_by_name": True, "extra": "ignore"}


class UserDataResponse(BaseModel):
    """Модель данных пользователя для GET /api/user."""

    id: str = Field(..., examples=["user-id-1"])
    name: str | None = Field(None, examples=["Александр"])
    last_name: str | None = Field(None, alias="lastName", examples=["Иванов"])
    birthdate: datetime.datetime | None = Field(None, examples=["1990-01-29T08:40:07.590Z"])
    status: Literal["Начинающий", "Опытный"] | None = None
    base_locations: list[Location] = Field(default_factory=list, alias="baseLocations")
    educations: list[Education] = Field(default_factory=list)
    additional_info: str | None = Field(
        None, alias="additionalInfo", examples=["Дополнительная информация o пользователе."]
    )
    contacts: Contacts | None = None
    favourite_requests: list[str] = Field(default_factory=list, alias="favouriteRequests")

    model_config = {"extra": "ignore", "populate_by_name": True}
