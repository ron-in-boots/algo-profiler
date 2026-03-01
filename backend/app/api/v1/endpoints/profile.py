from fastapi import APIRouter, HTTPException
from app.models.request_models import ProfileRequest
from app.models.response_models import ProfileResponse
from app.core.code_validator import validate_code
from app.core.compiler import inject_template
from app.core.executor import run_profile
from app.core.complexity import classify_complexity

router = APIRouter()

@router.post("/profile", response_model=ProfileResponse)
async def profile_code(request: ProfileRequest):
    # Step 1: Validate
    is_safe, error_msg = validate_code(request.code, request.input_type)
    if not is_safe:
        raise HTTPException(status_code=422, detail={
            "error": "validation_failed",
            "message": error_msg
        })

    # Step 2: Inject into template
    full_source = inject_template(request.code, request.input_type)

    # Step 3: Profile via Docker
    measurements = run_profile(
        source_code=full_source,
        sizes=request.sizes,
        input_type=request.input_type,
        data_type=request.data_type
    )

    # Step 4: Classify
    complexity = classify_complexity(measurements)

    return ProfileResponse(measurements=measurements, complexity=complexity)
