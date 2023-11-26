from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant


async def get_exams_details(cookie):
    url = constant.UMS_EXAM_SEATING_PLAN_URL
    headers = constant.USER_AGENT_ONLY
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            trs = soup.find_all(
                "tr",
                id=lambda x: x
                and x.startswith("ctl00_cphHeading_gvDisplaySeatingPlan_ctl00__"),
            )
            exams = {"exams": []}
            for tr in trs:
                tds = tr.find_all("td")
                course_code = tds[0].get_text(strip=True)
                course_name = tds[1].get_text(strip=True)
                exam_type = tds[2].get_text(strip=True)
                room_no = tds[3].get_text(strip=True)
                reporting_time = tds[4].get_text(strip=True)
                date = tds[5].get_text(strip=True)
                time = tds[6].get_text(strip=True)
                detainee_status = tds[7].get_text(strip=True)
                defaulter_detail = tds[8].get_text(strip=True)
                exams["exams"].append(
                    {
                        "course_code": course_code,
                        "course_name": course_name,
                        "exam_type": exam_type,
                        "room_no": room_no,
                        "reporting_time": reporting_time,
                        "date": date,
                        "time": time,
                        "detainee_status": detainee_status,
                        "defaulter_detail": defaulter_detail,
                    }
                )
            soup.decompose()
            await session.close()
            return exams
