from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
import json


async def get_placement_drives(cookie):
    url = constant.UMS_PLACEMENT_DRIVES_URL
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps({})) as res:
            html = await res.json()
            soup = BeautifulSoup(html["d"], "lxml")
            placement_divs = soup.find_all("div", class_="mycoursesdiv")
            placements = {"drives": []}
            for placement_div in placement_divs:
                list_of_divs = placement_div.find_all("div")
                company_name = list_of_divs[0].get_text(strip=True)
                list_of_p_s = list_of_divs[-1].find_all("p")
                if len(list_of_p_s) == 1:
                    stream = list_of_p_s[0].get_text(strip=True)
                elif len(list_of_p_s) == 2:
                    stream = list_of_p_s[0].get_text(strip=True)
                    salary = list_of_p_s[1].get_text(strip=True)
                placements["drives"].append(
                    {"company_name": company_name, "stream": stream, "salary": salary}
                )
            soup.decompose()
            await session.close()
            return placements
