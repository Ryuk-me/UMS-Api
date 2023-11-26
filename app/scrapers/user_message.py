from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
from app.utilities.clean_str_regex import regex_replace_str
import json


async def get_user_messages(cookie):
    url = constant.UMS_USER_MESSAGES
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps({})) as res:
            html = await res.json()
            soup = BeautifulSoup(html["d"], "lxml")
            msg_list = {"messages": []}
            divs = soup.find_all("div", class_="right-arrow")
            ps = soup.find_all("p", class_="text-muted")
            for idx in range(len(divs)):
                my_dict = {}
                title = regex_replace_str(divs[idx].get_text(strip=True))
                desc = regex_replace_str(ps[idx].get_text(strip=True))
                my_dict["title"] = title
                my_dict["message"] = desc
                msg_list["messages"].append(my_dict)
            await session.close()
            return msg_list
