from fastapi import APIRouter

router = APIRouter(prefix="/doc", tags=["docs"])


@router.get("/", response_model=str, description="Get information about the project.")
async def project_info():
    return "Project is running"
