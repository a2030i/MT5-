"""endpoints المستخدمين"""
from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.schemas.schemas import UserResponse


router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(user: CurrentUser):
    """معلومات المستخدم الحالي"""
    return user
