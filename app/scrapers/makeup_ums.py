from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant


async def get_makeup_classes(cookie):
    url = constant.UMS_MAKEUP_CLASSES_URL
    headers = constant.USER_AGENT_ONLY
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=headers,
        ) as res:
            #! This will get us first event and view state
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")

            makeups = {"makeup": []}
            table = soup.find("table", class_="aspGridView")
            if table == None:
                return makeups
            for tr in table.find_all("tr")[1:]:
                makeup_obj = {
                    "category": None,
                    "scheduled_date": None,
                    "lecture_time": None,
                    "room_no": None,
                    "section": None,
                    "group_no": None,
                    "course_code": None,
                    "attendance_type": None,
                    "taken_by": None,
                    "uid": None,
                }
                td = tr.find_all("td")
                makeup_obj["category"] = td[0].get_text(strip=True)
                makeup_obj["scheduled_date"] = td[1].get_text(strip=True)
                makeup_obj["lecture_time"] = td[2].get_text(strip=True)
                makeup_obj["room_no"] = td[3].get_text(strip=True)
                makeup_obj["section"] = td[4].get_text(strip=True)
                makeup_obj["group_no"] = td[5].get_text(strip=True)
                makeup_obj["course_code"] = td[6].get_text(strip=True)
                makeup_obj["attendance_type"] = td[7].get_text(strip=True)

                name_nd_uid = td[8].get_text(strip=True).split(":")
                name = name_nd_uid[0].strip()
                uid = name_nd_uid[-1].strip()
                makeup_obj["taken_by"] = name
                makeup_obj["uid"] = uid
                makeups["makeup"].append(makeup_obj)
            soup.decompose()
            await session.close()
            return makeups
