from fastapi import APIRouter
from app.Config import settings
from fastapi import Depends, status
from app.schema import user_schema
from app.scrapers.ums_home_today_class import get_todays_class_and_attendance
from app.scrapers.get_time_table import get_time_table_details
from app.scrapers.makeup_ums import get_makeup_classes
from app import services
from typing import Annotated


router = APIRouter(
    prefix=settings.BASE_API_V1 + "/timetable",
    tags=["Time Table and Make Up Route"],
    redirect_slashes=False,
)


@router.post("/classes", status_code=status.HTTP_200_OK)
async def time_table_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ]
):
    """
    Return user's time table.
    """
    res = await get_time_table_details(user.cookie)
    res["cookie"] = user.cookie
    return res


@router.post("/makeup", status_code=status.HTTP_200_OK)
async def make_up_class_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ]
):
    """
    Return makeup classes.
    """
    makeup_details = await get_makeup_classes(user.cookie)
    makeup_details["cookie"] = user.cookie
    return makeup_details


#!  It will give user's TODAYS TIME TABLE AND ROLL NO. AND SECTION
@router.post("/today", status_code=status.HTTP_200_OK)
async def get_user_today_time_table_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ]
):
    """
    Returns today classess with Attendance status.
    """
    res = await get_todays_class_and_attendance(user.cookie)
    res["cookie"] = user.cookie
    return res
