from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    print('here')
    return "App is Healthy."