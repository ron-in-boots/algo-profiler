from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.llm_service import analyze_code

router = APIRouter()

class AnalyzeRequest(BaseModel):
    code: str
    measurements: List[Dict[str, Any]]
    complexity: Dict[str, Any]

class AnalyzeResponse(BaseModel):
    analysis: str

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    try:
        analysis = analyze_code(
            code=request.code,
            measurements=request.measurements,
            complexity=request.complexity
        )
        return AnalyzeResponse(analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
