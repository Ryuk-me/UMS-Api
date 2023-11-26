from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
import json


async def get_attendance_summary(cookie):
    url = constant.UMS_ATTENDANCE_SUMMARY_URL
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps({})) as res:
            html = await res.json()
            soup = BeautifulSoup(html["d"], "lxml")
            attendance = {"summary": [], "attendance_details": None}
            trs = soup.find_all("tr")[0::2]
            for idx, tr in enumerate(trs):
                tds = tr.find_all("td")
                if idx == len(trs) - 1:
                    obj = {}
                    obj["total_duty_leaves"] = tds[2].get_text(strip=True)
                    obj["total_lectures_attended"] = tds[4].get_text(strip=True)
                    obj["total_lectures_delivered"] = tds[3].get_text(strip=True)
                    obj["total_agg_attendance"] = tds[5].get_text(strip=True)
                    attendance["attendance_details"] = obj
                    break
                subject_name_and_code = tds[0].get_text(strip=True).split(":")
                subject_code = subject_name_and_code[0]
                subject_name = subject_name_and_code[-1]
                last_attended = tds[1].get_text(strip=True)
                duty_leave = tds[2].get_text(strip=True)
                total_delivered = tds[3].get_text(strip=True)
                total_attended = tds[4].get_text(strip=True)
                agg_attendance = tds[5].get_text(strip=True)
                attendance["summary"].append(
                    {
                        "subject_code": subject_code,
                        "subject_name": subject_name,
                        "last_attended": last_attended,
                        "duty_leaves": duty_leave,
                        "total_attended": total_attended,
                        "total_delivered": total_delivered,
                        "agg_attendance": agg_attendance,
                    }
                )
            soup.decompose()
            await session.close()
            return attendance


async def get_attendance_detail(cookie):
    url = constant.UMS_ATTENDANCE_DETAILS_URL
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps({})) as res:
            html = await res.json()
            soup = BeautifulSoup(html["d"], "lxml")
            divs = soup.find_all("div", class_="border")
            attendance_details = {}
            for div in divs:
                course_code_and_text = div.find("p", class_="main-heading").get_text(
                    strip=True
                )
                course_code = course_code_and_text.split(":")[-1].strip()
                attendance_details[course_code] = []
                div_id_dynamic = "collapse" + course_code
                selected_div = div.find("div", id=div_id_dynamic)
                trs = selected_div.find("tbody").find_all("tr")
                for tr in trs:
                    tds = tr.find_all("td")
                    date = tds[0].get_text(strip=True)
                    timing = tds[1].get_text(strip=True)
                    type = tds[2].get_text(strip=True)
                    attendance = tds[3].get_text(strip=True)
                    faculty_name = tds[4].get_text(strip=True)
                    block_reason = tds[5].get_text(strip=True)
                    attendance_details[course_code].append(
                        {
                            "date": date,
                            "timing": timing,
                            "type": type,
                            "attendance": attendance,
                            "faculty_name": faculty_name,
                            "block_reason": block_reason,
                        }
                    )
            soup.decompose()
            await session.close()
            return attendance_details
