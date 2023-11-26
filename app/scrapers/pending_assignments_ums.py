from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
import json


async def get_pending_assignments(cookie):
    url = constant.UMS_PENDING_ASSIGNMENTS_URL
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps({})) as res:
            html = await res.json()
            soup = BeautifulSoup(html["d"], "lxml")

            pending_assignments = {"assignments": []}
            assignments_divs = soup.find_all("div", class_="mycoursesdiv")
            for assignment_div in assignments_divs:
                course_code = assignment_div.find("div", class_="right-arrow").get_text(
                    strip=True
                )
                assignment_name = assignment_div.find("p").get_text(strip=True)
                pending_assignments["assignments"].append(
                    {"course_code": course_code, "assignment_name": assignment_name}
                )
            soup.decompose()
            await session.close()
            return pending_assignments
