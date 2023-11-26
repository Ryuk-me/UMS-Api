from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
import json


async def get_user_syllabus_with_attendance(cookie):
    url = constant.UMS_USER_COURSE_SYLLABUS
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps({})) as res:
            html = await res.json()
            soup = BeautifulSoup(html["d"], "lxml")

            divs = soup.find_all("div", class_="mycoursesdiv")
            courses_list = {"course": {}}
            for div in divs:
                attendance = div.find("span").get_text(strip=True)
                course_name_and_code = div.find("p").get_text(strip=True).split(":")
                course_name = course_name_and_code[-1]
                course_code = course_name_and_code[0]
                syllabus_href = (
                    "https://ums.lpu.in/lpuums/" + div.find_all("a")[1]["href"]
                )
                courses_list["course"][course_code] = {
                    "course_name": course_name,
                    "course_code": course_code,
                    "agg_attendance": attendance,
                    "syllabus": syllabus_href,
                }
            soup.decompose()
            await session.close()
            return courses_list
