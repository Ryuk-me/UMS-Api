import requests
from fastapi import APIRouter
from app.Config import settings
from fastapi import Depends, status
from app.schema import user_schema
from app import services
from app.scrapers.placement_drives_ums import get_placement_drives
from app import error_status
from typing import Annotated
from app.Config import settings

router = APIRouter(
    prefix=settings.BASE_API_V1 + "/misc",
    tags=["Miscellaneous routes"],
    redirect_slashes=False,
)


@router.post("/drives", status_code=status.HTTP_200_OK)
async def placemet_drive_route(
    user: Annotated[
        user_schema.UserRequests, Depends(services.dependency_verify_cookie_ums_home)
    ]
):
    """
    Returns today happened drives.
    """
    res = await get_placement_drives(user.cookie)
    res["cookie"] = user.cookie
    return res


#! Search user from lpu using Reg_no or Name
@router.get("/search_user/", status_code=status.HTTP_200_OK)
def search_user_from_lpu_live_route(id: str):
    """
    Returns user/s details from lpu live with the help of name/UID
    """
    url = "https://lpulive.lpu.in/fugu-api/api/chat/groupChatSearch?en_user_id={}&search_text={}&user_role=USER".format(
        settings.LPU_LIVE_TOKEN, id
    )
    try:
        res = requests.get(
            url, headers={"app_version": "1.0.0", "device_type": "WEB"}
        ).json()
        users = res["data"]["users"]
        if len(users) == 0:
            return {"detail": "No user found."}

        return {"users": users}
    except:
        raise error_status.LPU_LIVE_SEARCH_ERROR
