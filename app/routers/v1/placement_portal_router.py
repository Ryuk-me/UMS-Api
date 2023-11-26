from fastapi import APIRouter
from app.Config import settings
from fastapi import Depends, status
from app.schema import user_schema
from app import services
from app.scrapers.login_ums import placement_login
from typing import Annotated
from app.scrapers.placement_portal import get_home_page_details, get_placement_drives


router = APIRouter(
    prefix=settings.BASE_API_V1 + "/placement",
    tags=["Placement Portal Routes"],
    redirect_slashes=False,
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=user_schema.Token)
async def placement_portal_login(user: user_schema.UserLogin):
    """
    Returns an authenticated placement session cookie.
    """
    cookie = await placement_login(user)
    return {"cookie": cookie}


@router.post("/", status_code=status.HTTP_200_OK)
async def get_placement_portal_home_details(
    user: Annotated[
        user_schema.UserRequests,
        Depends(services.dependency_verify_cookie_placement_portal),
    ],
):
    """
    Return placement portal home page details containing recent drives and fines.
    """
    res = await get_home_page_details(user.cookie)
    res["cookie"] = user.cookie
    return res


@router.post("/drives", status_code=status.HTTP_200_OK)
async def get_placement_drives_details(
    user: Annotated[
        user_schema.UserRequests,
        Depends(services.dependency_verify_cookie_placement_portal),
    ],
):
    """
    Returns All eligible drives details.
    """
    res = await get_placement_drives(user.cookie)
    res["cookie"] = user.cookie
    return res
