from typing import Any
from pydantic import BaseModel


class TaskGenerationPayload(BaseModel):
    title: str | None = None
    url: str | None = None
    webhook_callback_url: str | None = None
    navigation_goal: str | None = None
    data_extraction_goal: str | None = None
    proxy_location: str | None = None
    navigation_payload: dict[str, Any] | None = None
    extracted_information_schema: dict[str, Any] | None = None
    totp_verification_url: str | None = None
    totp_identifier: str | None = None
    error_code_mapping: str | None = None
