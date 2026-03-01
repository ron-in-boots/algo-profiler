from pydantic import BaseModel, field_validator
from typing import List, Optional

class ProfileRequest(BaseModel):
    code: str
    input_type: str = "array"
    data_type: str = "random"
    sizes: Optional[List[int]] = None

    @field_validator("code")
    @classmethod
    def code_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Code cannot be empty")
        if len(v) > 65536:
            raise ValueError("Code too large")
        return v

    @field_validator("input_type")
    @classmethod
    def valid_input_type(cls, v):
        allowed = ["array", "string", "graph", "matrix"]
        if v not in allowed:
            raise ValueError(f"input_type must be one of {allowed}")
        return v

    @field_validator("data_type")
    @classmethod
    def valid_data_type(cls, v):
        allowed = ["random", "sorted", "reverse_sorted", "nearly_sorted"]
        if v not in allowed:
            raise ValueError(f"data_type must be one of {allowed}")
        return v
