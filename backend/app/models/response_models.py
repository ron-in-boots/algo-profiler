from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SingleMeasurement(BaseModel):
    n: int
    time_ms: Optional[float]
    status: str
    error: Optional[str] = None

class ProfileResponse(BaseModel):
    measurements: List[SingleMeasurement]
    complexity: Dict[str, Any]
    status: str = "ok"
