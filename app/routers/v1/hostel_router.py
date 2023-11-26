from fastapi import APIRouter, Response
from app.Config import settings
from fastapi import Depends, status
from app.schema import user_schema
from app import services
from app.scrapers.hostel_electricity_ums import get_hosteler_details
from app.scrapers.hostel_leave_slip_ums import get_hostel_leave_slip
from typing import Annotated

router = APIRouter(
    prefix=settings.BASE_API_V1 + "/hostel",
    tags=["Hostel Routes"],
    redirect_slashes=False,
)


@router.post("/", status_code=status.HTTP_200_OK)
async def hostel_details_with_electric_consumption_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ]
):
    """
    Returns user's details with electricity consumption (if user is a hosteler)
    """
    res = await get_hosteler_details(user.cookie)
    res["cookie"] = user.cookie
    return res


@router.post("/leave_slip", status_code=status.HTTP_200_OK)
async def hostel_leave_slip_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
    response: Response,
):
    """
    Returns leave slip base64 that can be converted into image if there is any leave slip available
    """
    res = await get_hostel_leave_slip(user.cookie)
    if res is None:
        res = {}
        res["detail"] = "Leave Slip Not Found"
        res["cookie"] = user.cookie
        response.status_code = status.HTTP_404_NOT_FOUND
        return res
    res["cookie"] = user.cookie
    return res
