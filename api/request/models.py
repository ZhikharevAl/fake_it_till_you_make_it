import datetime
from typing import Literal

from pydantic import AnyUrl, BaseModel, EmailStr, Field

from api.user.models import Location


class Organization(BaseModel):
    """Модель организации (из HelpRequestData)."""

    title: str | None = Field(None, examples=["Благотворительная организация"])
    is_verified: bool | None = None


class ActionStep(BaseModel):
    """Модель шага в плане действий (из HelpRequestData)."""

    step_label: str | None = Field(None, examples=["Шаг 1"])
    is_done: bool | None = None


class RequestContacts(BaseModel):
    """Модель контактов для запроса помощи (из HelpRequestData)."""

    email: EmailStr | None = Field(None, examples=["contact@example.com"])
    phone: str | None = Field(None, examples=["+123456789"])
    website: AnyUrl | None = Field(None, examples=["https://example.com"])


class HelperRequirements(BaseModel):
    """Модель требований к помощнику (из HelpRequestData)."""

    helper_type: Literal["group", "single"] | None = None
    is_online: bool | None = None
    qualification: Literal["professional", "common"] | None = None


class HelpRequestData(BaseModel):
    """Модель данных запроса помощи ."""

    id: str = Field(..., examples=["request-id-1"])
    title: str | None = Field(None, examples=["Помощь в проекте"])
    organization: Organization | None = None
    description: str | None = Field(None, examples=["Описание запроса на помощь."])
    goal_description: str | None = Field(None, examples=["Цель данного запроса."])
    actions_schedule: list[ActionStep] = Field(default_factory=list)
    ending_date: datetime.date | None = Field(None, examples=["2023-12-31"])
    location: Location | None = None
    contacts: RequestContacts | None = None
    requester_type: Literal["person", "organization"] | None = None
    help_type: Literal["finance", "material"] | None = None
    helper_requirements: HelperRequirements | None = None
    contributors_count: int | None = Field(None, examples=[10])
    request_goal: int | None = Field(None, examples=[10000])
    request_goal_current_value: int | None = Field(None, examples=[2500])


RequestsListResponse = list[HelpRequestData]
