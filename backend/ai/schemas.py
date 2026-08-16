from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class DeadlineType(str, Enum):
    EXACT = "exact"
    RANGE = "range"
    RELATIVE = "relative"
    CONDITIONAL = "conditional"


class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Severity(str, Enum):
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class ActionSchema(BaseModel):
    title: str
    description: str
    deadline: Optional[str] = None
    deadline_type: Optional[str] = "exact"
    priority: str = "MEDIUM"
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    source_page: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class FeeSchema(BaseModel):
    amount: float
    currency: str = "INR"
    purpose: str
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    source_page: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class RiskSchema(BaseModel):
    description: str
    severity: str = "WARNING"
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    source_page: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PersonSchema(BaseModel):
    name: str
    role: Optional[str] = None
    department: Optional[str] = None
    organization: Optional[str] = None
    source_page: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ExtractionResponse(BaseModel):
    summary: str
    actions: List[ActionSchema] = []
    fees: List[FeeSchema] = []
    risks: List[RiskSchema] = []
    required_documents: List[str] = []
    people: List[PersonSchema] = []

    model_config = ConfigDict(from_attributes=True)


def classify_confidence(score: float) -> str:
    """
    Classifies confidence score into HIGH, MEDIUM, or NEEDS VERIFICATION.
    - >= 0.85: HIGH
    - 0.60 – 0.84: MEDIUM
    - < 0.60: NEEDS VERIFICATION
    """
    if score >= 0.85:
        return "HIGH"
    elif score >= 0.60:
        return "MEDIUM"
    else:
        return "NEEDS VERIFICATION"
