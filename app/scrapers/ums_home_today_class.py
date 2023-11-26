#! It will send back today's class and  user's Roll_No mapped with course Code
from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant


async def get_todays_class_and_attendance(cookie):
    url = constant.UMS_HOME_PAGE_URL
    headers = constant.USER_AGENT_ONLY
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=headers,
        ) as res:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            today_time_table_trs = soup.find_all("tbody", class_="table-hover")[
                0
            ].find_all("tr")
            obj = {"today_time_table": [], "misc_details": {}}
            for tr in today_time_table_trs:
                tds = tr.find_all("td")
                timing = tds[0].get_text(strip=True)
                course_code = tds[1].get_text(strip=True)
                room_number = tds[2].get_text(strip=True)
                attendance_status = tds[3].get_text(strip=True)
                obj["today_time_table"].append(
                    {
                        "timing": timing,
                        "course_code": course_code,
                        "room_number": room_number,
                        "attendance_status": attendance_status,
                    }
                )

            misc_details_div = soup.find("div", class_="tab_scroll").find_all(
                "div", class_="skillbar"
            )
    for misc_div in misc_details_div:
        spans = misc_div.find_all("span")
        roll_no = spans[0].get_text(strip=True)
        course_code = spans[1].get_text(strip=True).split("(")[0]
        subject_name = spans[2].get_text(strip=True)
        agg_attendance = spans[-1].get_text(strip=True)
        obj["misc_details"][course_code] = {
            "course_code": course_code,
            "subject_name": subject_name,
            "agg_attendance": agg_attendance + "%",
            "roll_no": roll_no,
            "section": roll_no[1:6],
        }
    am_entries = []
    pm_entries = []

    for entry in obj["today_time_table"]:
        if "AM" in entry["timing"]:
            am_entries.append(entry)
        else:
            pm_entries.append(entry)

    # Sort each group based on time
    am_sorted = sorted(am_entries, key=lambda x: x["timing"])
    pm_sorted = sorted(pm_entries, key=lambda x: x["timing"])

    # Combine the sorted groups
    sorted_time_table_list = am_sorted + pm_sorted

    # Create a new dictionary with the sorted list
    sorted_time_table_dict = {"today_time_table": sorted_time_table_list}
    obj["today_time_table"] = sorted_time_table_dict["today_time_table"]
    soup.decompose()
    await session.close()
    return obj
