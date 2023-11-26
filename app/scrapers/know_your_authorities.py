from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
import json


async def get_user_heads(cookie):
    url = constant.UMS_KNOW_YOUR_AUTHORITIES_URL
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps({})) as res:
            html = await res.json()
            soup = BeautifulSoup(html["d"], "lxml")
            dash = "https://ums.lpu.in/lpuums/"
            k_ur_authorities = {"authorities": []}
            divs = soup.find_all("div", class_="item")
            for div in divs:
                img = div.find("img")["src"]
                if str(img).startswith("Dash"):
                    img = dash + img
                details = (
                    div.select_one("div.row").select_one("div.row").find_all("div")
                )
                role = details[0].get_text(strip=True)
                faculty_name = details[1].get_text(strip=True)
                faculty_designation = details[2].get_text(strip=True)
                branch = details[3].get_text(strip=True)
                try:
                    phone_no = details[4].get_text(strip=True).replace("NA", "")
                except:
                    phone_no = None
                k_ur_authorities["authorities"].append(
                    {
                        "faculty_name": faculty_name,
                        "faculty_designation": faculty_designation,
                        "role": role,
                        "branch": branch,
                        "phone_no": phone_no,
                        "profile_image": img,
                    }
                )
            soup.decompose()
            await session.close()
            return k_ur_authorities
