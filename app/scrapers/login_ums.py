from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
from app.schema.user_schema import UserLogin
from app import error_status
import json


async def login_using_reg_no_ums_home(user: UserLogin):
    url = constant.UMS_LOGIN_URL
    headers = constant.USER_AGENT_FORM_URL_ENCODED
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=headers,
        ) as res:
            #! This will get us first event and view state
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            __LASTFOCUS = ""
            __EVENTTARGET = ""
            __EVENTARGUMENT = ""
            __VIEWSTATE = soup.find("input", {"id": "__VIEWSTATE"})["value"]
            __VIEWSTATEGENERATOR = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})[
                "value"
            ]
            __SCROLLPOSITIONX = "0"
            __SCROLLPOSITIONY = "0"
            __EVENTVALIDATION = soup.find("input", {"id": "__EVENTVALIDATION"})["value"]
            txtU = user.reg_no
            TxtpwdAutoId_8767 = user.password
            DropDownList1 = "1"
            ddlStartWith = "StudentDashboard.aspx"
            iBtnLogins_x = "40"
            iBtnLogins_y = "50"

            #! Payload just with reg_number.
            payload_with_reg_no_only = {
                "__LASTFOCUS": __LASTFOCUS,
                "__EVENTTARGET": "txtU",
                "__EVENTARGUMENT": __EVENTARGUMENT,
                "__VIEWSTATE": (__VIEWSTATE),
                "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                "__SCROLLPOSITIONX": __SCROLLPOSITIONX,
                "__SCROLLPOSITIONY": __SCROLLPOSITIONY,
                "__EVENTVALIDATION": (__EVENTVALIDATION),
                "txtU": txtU,
                "TxtpwdAutoId_8767": "",
                "DropDownList1": DropDownList1,
            }
            soup.decompose()
            #! Here we will make a post request just with the user id and it will give us updated states
            async with session.post(
                url, headers=headers, data=payload_with_reg_no_only
            ) as res:
                html = await res.text()
                soup = BeautifulSoup(html, "lxml")

                __VIEWSTATE = soup.find("input", {"id": "__VIEWSTATE"})["value"]
                __VIEWSTATEGENERATOR = soup.find(
                    "input", {"id": "__VIEWSTATEGENERATOR"}
                )["value"]
                __SCROLLPOSITIONX = "0"
                __SCROLLPOSITIONY = "0"
                __EVENTVALIDATION = soup.find("input", {"id": "__EVENTVALIDATION"})[
                    "value"
                ]

                #! Payload with updated state and Password
                payload = {
                    "__LASTFOCUS": __LASTFOCUS,
                    "__EVENTTARGET": __EVENTTARGET,
                    "__EVENTARGUMENT": __EVENTARGUMENT,
                    "__VIEWSTATE": (__VIEWSTATE),
                    "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                    "__SCROLLPOSITIONX": __SCROLLPOSITIONX,
                    "__SCROLLPOSITIONY": __SCROLLPOSITIONY,
                    "__EVENTVALIDATION": (__EVENTVALIDATION),
                    "txtU": txtU,
                    "TxtpwdAutoId_8767": TxtpwdAutoId_8767,
                    "ddlStartWith": ddlStartWith,
                    "iBtnLogins150203125": "Login",
                    # "iBtnLogins.x": iBtnLogins_x,
                    # "iBtnLogins.y": iBtnLogins_y,
                }
                soup.decompose()
                #! SignIn with updated payload
                async with session.post(url, headers=headers, data=payload) as res:
                    asp_cookie = None
                    try:
                        asp_cookie = res.request_info.headers["Cookie"]
                    except:
                        await session.close()
                        raise error_status.SOMETHING_WRONG_WITH_UMS_SERVER
                    await session.close()
                    is_auth = await check_auth_status_ums_home(asp_cookie)
                    if is_auth:
                        return asp_cookie
                    raise error_status.CREDENTIALS_NOT_VALID


async def placement_login(user: UserLogin):
    url = constant.UMS_PLACEMENT_LOGIN
    headers = constant.USER_AGENT_FORM_URL_ENCODED
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=headers,
        ) as res:
            #! This will get us first event and view state
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            __VIEWSTATE = soup.find("input", {"id": "__VIEWSTATE"})["value"]
            __VIEWSTATEGENERATOR = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})[
                "value"
            ]
            __EVENTVALIDATION = soup.find("input", {"id": "__EVENTVALIDATION"})["value"]

            #! Payload just with reg_number.
            payload_with_reg_no_only = {
                "__VIEWSTATE": __VIEWSTATE,
                "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                "__EVENTVALIDATION": (__EVENTVALIDATION),
                "txtUserName": user.reg_no,
                "txtPassword": user.password,
                "Button1": "Login",
            }
            soup.decompose()
            #! Here we will make a post request just with the user id and it will give us updated states
            async with session.post(
                url, headers=headers, data=payload_with_reg_no_only
            ) as res:
                html = await res.text()
                #! SignIn with updated payload
                try:
                    asp_cookie = res.request_info.headers["Cookie"]
                except:
                    await session.close()
                    raise error_status.SOMETHING_WRONG_WITH_UMS_SERVER
                await session.close()
                is_auth = await check_auth_status_placement_portal(asp_cookie)
                if is_auth:
                    return asp_cookie
                raise error_status.CREDENTIALS_NOT_VALID


async def check_auth_status_ums_home(cookie) -> bool:
    async with aiohttp.ClientSession() as session:
        headers = constant.USER_AGENT_JSON
        headers["Cookie"] = cookie
        resp = await session.post(
            constant.UMS_STUDENT_PHONE_NUMBER_URL,
            headers=headers,
            data=json.dumps({}),
        )
        rs_json = await resp.json()
        await session.close()
        if rs_json.get("d", {}) is None:
            return False
        return True


async def check_auth_status_placement_portal(cookie) -> bool:
    async with aiohttp.ClientSession() as session:
        headers = constant.USER_AGENT_FORM_URL_ENCODED
        headers["Cookie"] = cookie
        resp = await session.get(
            constant.UMS_PLACEMENT_PORTAL_HOME_PAGE, headers=headers
        )
        html = await resp.text()
        await session.close()
        soup = BeautifulSoup(html, "lxml")
        title = soup.find("title").get_text(strip=True)
        if title and "Home" in title:
            return True
        return False
