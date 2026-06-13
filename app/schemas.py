from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field

Gender = Literal["male", "female"]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str


class UserResponse(BaseModel):
    user_id: str
    email: str
    subscription_tier: str
    has_imprint: bool = False


class BirthProfileCreate(BaseModel):
    display_name: str = Field(min_length=1, max_length=120)
    birth_datetime_local: datetime
    timezone: str = Field(description="IANA timezone, e.g. America/New_York")
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    birth_place_label: str = ""
    gender: Gender = "male"


class BirthProfileResponse(BirthProfileCreate):
    id: str
    created_at: datetime


class ImprintResponse(BaseModel):
    id: str
    user_id: str
    schema_version: str
    computed_at: datetime
    birth_fingerprint: str
    imprint: dict[str, Any]


class ImprintMeResponse(ImprintResponse):
    overview: dict[str, Any] | None = None
    chart_readings: dict[str, Any] | None = None


class ImprintPreviewResponse(BaseModel):
    imprint: dict[str, Any]
    chart_readings: dict[str, Any] | None = None


class DailyPreviewRequest(BaseModel):
    imprint: dict[str, Any]
    target_date: str | None = None


class ZeroPastTestRequest(BaseModel):
    imprint: dict[str, Any] | None = None  # for preview mode
    past_date: str  # YYYY-MM-DD
    event_description: str = Field(min_length=10, max_length=2000)
    previous_analysis: str | None = None
    feedback: str | None = None
    round: int = 1


class SealImprintRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    commonly_known_as: str | None = Field(default=None, max_length=120)
    birth_datetime_local: datetime
    place_of_birth: str = Field(min_length=2, max_length=255)
    gender: Gender = "male"
    timezone: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class ZeroChatRequest(BaseModel):
    user_id: str
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str | None = None


class ZeroChatResponse(BaseModel):
    conversation_id: str
    reply: str
    model: str
    context_snapshot: dict[str, Any]


class ZeroMemoryCreate(BaseModel):
    user_id: str
    note: str = Field(min_length=1, max_length=2000)


class ZeroMemoryResponse(BaseModel):
    id: str
    user_id: str
    note: str
    created_at: datetime


class VehicleInput(BaseModel):
    plate: str | None = None
    model_year: int | None = Field(default=None, ge=1900, le=2100)
    label: str = "Vehicle"


class LocationInsightRequest(BaseModel):
    user_id: str
    state_code: str | None = Field(default=None, max_length=2)
    city_name: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    include_companies: bool = True
    include_narration: bool = True
    vehicle: VehicleInput | None = None


class LocationInsightResponse(BaseModel):
    user_id: str
    insight: dict[str, Any]
    narrative: str | None = None
    model: str | None = None