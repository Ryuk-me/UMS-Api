from fastapi import APIRouter
from app.Config import settings
from fastapi import Depends, status
from app.schema import user_schema
from app.scrapers.announcements_ums import get_all_annoucements
from app import services
from typing import Annotated

router = APIRouter(
    prefix=settings.BASE_API_V1 + "/annoucements",
    tags=["Announcements"],
    redirect_slashes=False,
)


@router.post("/", status_code=status.HTTP_200_OK)
async def get_all_announcements_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ]
):
    """
    Returns recent announcements
    """
    resp = await get_all_annoucements(user.cookie)
    resp["cookie"] = user.cookie
    return resp
