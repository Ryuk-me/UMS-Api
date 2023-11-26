from fastapi import APIRouter, Depends
from app.Config import settings
from typing import Annotated
from fastapi import status
from app.schema import user_schema
from app.scrapers.login_ums import (
    login_using_reg_no_ums_home,
)
from app.scrapers.user_message import get_user_messages
from app.scrapers.user_course_syllabus import get_user_syllabus_with_attendance
from app.scrapers.know_your_authorities import get_user_heads
from app.scrapers.attendance_summary import (
    get_attendance_summary,
    get_attendance_detail,
)
from app.scrapers.assignments_ums import get_all_assignments_and_marks
from app.scrapers.exams_ums import get_exams_details
from app.scrapers.pending_assignments_ums import get_pending_assignments
from app.scrapers.cgpa_term_wise import get_cgpa_term_wise
from app.scrapers.marks_term_wise import get_marks_term_wise
from app import services
import asyncio

router = APIRouter(
    prefix=settings.BASE_API_V1 + "/user", tags=["User Route"], redirect_slashes=False
)


#! USER CGPA, ATTENDANCE, SECTION Will be updated in DB, on every login request by user it will give basic user details
@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.Token,
)
async def login_user(user: user_schema.UserLogin):
    """
    Returns ums home authenticated cookie.
    """
    cookie = await login_using_reg_no_ums_home(user)
    return {"cookie": cookie}


#! GET CURRENT USER DETAILS
@router.post("/me", status_code=status.HTTP_200_OK, response_model=user_schema.UserOut)
async def current_user_details(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    """
    Returns current user details
    """
    user_details = await services.get_user_details(user)
    user_details["cookie"] = user.cookie
    return user_details


#! GET USER MESSAGES
@router.post("/messages", status_code=status.HTTP_200_OK)
async def get_user_messages_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    """
    Returns current user's message.
    """
    resp = await get_user_messages(user.cookie)
    resp["cookie"] = user.cookie
    return resp


#! SYLLABUS OF ALL SUBJECTS
@router.post("/syllabus", status_code=status.HTTP_200_OK)
async def get_user_syllabus_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    """
    Returns user's course with syllabus
    """
    syallabus = await get_user_syllabus_with_attendance(user.cookie)
    syallabus["cookie"] = user.cookie
    return syallabus


#! KNOW YOUR AUTHORITIES
@router.post("/authorities", status_code=status.HTTP_200_OK)
async def get_user_authorities_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    """
    Returns Authority Details.
    """
    resp = await get_user_heads(user.cookie)
    resp["cookie"] = user.cookie
    return resp


#!  It will give user's individual attendance
@router.post("/attendance", status_code=status.HTTP_200_OK)
async def get_user_individual_attendance_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    """
    Returns user's attendance details.
    """
    results = await asyncio.gather(
        get_attendance_summary(user.cookie),
        get_attendance_detail(user.cookie),
    )
    summary = results[0]
    details = results[1]
    for idx in range(len(summary["summary"])):
        sub_code = summary["summary"][idx]["subject_code"]
        list_of_attendance = details[sub_code]
        summary["summary"][idx]["detailed_attendance"] = list_of_attendance
    summary["cookie"] = user.cookie
    return summary


#!  It will give user's assignment
@router.post("/assignments", status_code=status.HTTP_200_OK)
async def get_user_assignments(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    res = await get_all_assignments_and_marks(user.cookie)
    res["cookie"] = user.cookie
    return res


#!  It will give user's available exams
@router.post("/exams", status_code=status.HTTP_200_OK)
async def get_user_exams(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    res = await get_exams_details(user.cookie)
    res["cookie"] = user.cookie
    return res


#!  It will give user's pending assignments
@router.post("/pending_assignments", status_code=status.HTTP_200_OK)
async def get_user_pending_assignments_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    res = await get_pending_assignments(user.cookie)
    res["cookie"] = user.cookie
    return res


#!  It will give user's CGPA TERM WISE
@router.post("/cgpa", status_code=status.HTTP_200_OK)
async def get_user_cgpa_term_wise_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    res = await get_cgpa_term_wise(user.cookie)
    res["cookie"] = user.cookie
    return res


#!  It will give user's MARKS TERM WISE
@router.post("/marks", status_code=status.HTTP_200_OK)
async def get_user_marks_term_wise_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ],
):
    res = await get_marks_term_wise(user.cookie)
    res["cookie"] = user.cookie
    return res
