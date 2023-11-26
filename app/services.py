from app.schema import user_schema
from app.constants import constant
import aiohttp
import json
from app.scrapers.login_ums import (
    check_auth_status_ums_home,
    login_using_reg_no_ums_home,
    check_auth_status_placement_portal,
    placement_login,
)
from app.utilities.clean_str_regex import regex_replace_str


async def get_user_details(user: user_schema.UserRequests):
    async with aiohttp.ClientSession() as session:
        headers = constant.USER_AGENT_JSON
        headers["Cookie"] = user.cookie
        resp = await session.post(
            constant.UMS_STUDENT_BASIC_INFO_URL,
            headers=headers,
            data=json.dumps({}),
        )
        rs_json = await resp.json()
        obj = rs_json["d"][0]
        new_user = {}
        new_user["registration_number"] = obj["Registrationnumber"]
        new_user["name"] = obj["StudentName"]
        new_user["program"] = regex_replace_str(obj["Program"])
        new_user["section"] = obj["Section"]
        new_user["profile_image"] = obj["StudentPicture"]
        new_user["dob"] = obj["DateofBirth"]
        new_user["cgpa"] = obj["CGPA"]
        new_user["agg_attendance"] = obj["AggAttendance"]
        new_user["roll_number"] = obj["RollNumber"]

        #! GET USER PHONE NUMBER
        resp = await session.post(
            constant.UMS_STUDENT_PHONE_NUMBER_URL,
            headers=headers,
            data=json.dumps({}),
        )
        rs_json = await resp.json()
        new_user["phone"] = rs_json["d"]
        return new_user


######################################
#
#    Dependencies
#
######################################


async def dependency_verify_cookie_ums_home(user: user_schema.UserRequests):
    is_auth = await check_auth_status_ums_home(user.cookie)
    if not is_auth:
        user.cookie = await login_using_reg_no_ums_home(user)
    return user


async def dependency_verify_cookie_placement_portal(user: user_schema.UserRequests):
    is_auth = await check_auth_status_placement_portal(user.cookie)
    if not is_auth:
        user.cookie = await placement_login(user)
    return user
