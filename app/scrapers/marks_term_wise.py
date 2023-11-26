from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
import json


async def get_marks_term_wise(cookie):
    url = constant.UMS_MARKS_TERM_WISE_URL
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps({})) as res:
            html = await res.json()
            soup = BeautifulSoup(html["d"], "lxml")
            term_divs = soup.find_all("div", class_="border")
            marks_term_wise = {}
            for term_div in term_divs:
                term_name_with_id = term_div.find("p", class_="main-heading").get_text(
                    strip=True
                )
                term_id = term_name_with_id.split(":")[-1].strip()
                marks_term_wise[term_id] = {}
                for div_detail in term_div.find_all("div", class_="divdetail"):
                    course_name = div_detail.find("h4").get_text(strip=True)
                    marks_term_wise[term_id][course_name] = []
                    trs = div_detail.find("tbody").find_all("tr")
                    for tr in trs:
                        tds = tr.find_all("td")
                        _type = tds[0].get_text(strip=True)
                        marks = tds[1].get_text(strip=True)
                        weightage = tds[2].get_text(strip=True)
                        marks_term_wise[term_id][course_name].append(
                            {"type": _type, "marks": marks, "weightage": weightage}
                        )
            soup.decompose()
            await session.close()
            return marks_term_wise
