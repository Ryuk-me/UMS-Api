import json
from enum import Enum
from bs4 import BeautifulSoup
from app.constants import constant
import aiohttp
from app.utilities.clean_str_regex import regex_replace_str


async def make_request(cookie):
    async with aiohttp.ClientSession() as session:
        header = constant.USER_AGENT_ONLY
        header["Cookie"] = cookie
        async with session.post(
            constant.UMS_STUDENT_TIME_TABLE,
            headers=header,
        ) as res:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            import re

            regx = re.compile(r"ReportViewerabcd\$ctl..\$Reserved_AsyncLoadTarget")

            mo = regx.search(html)
            state_v = str(mo.group())
            __VSTATE = soup.find("input", {"id": "__VSTATE"})["value"]
            __EVENTVALIDATION = soup.find("input", {"id": "__EVENTVALIDATION"})["value"]

            payload = {
                "ReportViewerabcd$ctl03$ctl00": "Refresh",
                "__EVENTTARGET": state_v,
                "__VSTATE": __VSTATE,
                "__EVENTVALIDATION": __EVENTVALIDATION,
            }
            is_On = True
            header = constant.USER_AGENT_ONLY
            header["Cookie"] = cookie
            counter = 1
            while is_On:
                async with session.post(
                    constant.UMS_STUDENT_TIME_TABLE, headers=header, data=payload
                ) as res:
                    html = await res.text()
                    soup = BeautifulSoup(html, "lxml")
                    title = soup.find("title").get_text(strip=True)
                    if not title.startswith("UMS"):
                        print("making request number " + str(counter) + " :")
                        if counter > 5:
                            return None
                        counter += 1
                        continue
                    is_On = False
                    soup.decompose()
                    await session.close()
                    return html


async def get_time_table_details(cookie):
    try:
        html = await make_request(cookie)
        soup = BeautifulSoup(html, "lxml")
        file = open("rohit_time.html", "w")
        file.write(html)
        file.close()
        tables = soup.select("td > table")

        legends = {
            "C": None,
            "F": None,
            "G": None,
            "R": None,
            "S": None,
        }

        legend_text = tables[6].get_text(strip=True).split(",")
        for e in legend_text:
            x = e.split("-")
            legends[x[0].strip()] = x[1].strip()

        section = tables[4].get_text(strip=True)
        last_updated = tables[10].get_text(strip=True)
        reg_no = tables[2].get_text(strip=True)

        #! TIME TABLE 11
        #! LEGENDS TEACHER 15
        #! TEACHERS CABIN 16

        class WeekDays(Enum):
            Monday = 1
            Tuesday = 2
            Wednesday = 3
            Thursday = 4
            Friday = 5
            Saturday = 6
            Sunday = 7

        WEEKS = {
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday",
            7: "Sunday",
        }

        time_table = {
            "time_table": {
                "Monday": {},
                "Tuesday": {},
                "Wednesday": {},
                "Thursday": {},
                "Friday": {},
                "Saturday": {},
                "Sunday": {},
            },
            "legends": legends,
            "section": section,
            "last_updated": last_updated,
            "registration_number": reg_no,
        }

        time_table_div = soup.find_all("div", class_=lambda x: x and x.endswith("100"))
        for time_div in time_table_div:
            timing = time_div.get_text(strip=True)
            for idx_week in range(1, 8):
                time_table["time_table"][WEEKS[idx_week]][timing] = ""

        for tr in tables[15].find_all("tr")[2:]:
            timing = None
            for idx, td in enumerate(tr.find_all("td")):
                div = td.find("div")
                subject_name = ""
                if not div == None:
                    import re

                    subject_name = div.get_text(strip=True)
                    subject_name = re.sub(" +", " ", subject_name)
                    subject_name = regex_replace_str(str(subject_name))
                if idx == 0:
                    timing = div.get_text(strip=True)
                elif WeekDays.Monday.value == idx:
                    if str(subject_name).startswith(
                        "Project Work/ Other Weekly Activities"
                    ):
                        subject_name = ""
                    time_table["time_table"]["Monday"][timing] = subject_name
                elif WeekDays.Tuesday.value == idx:
                    if str(subject_name).startswith(
                        "Project Work/ Other Weekly Activities"
                    ):
                        subject_name = ""
                    time_table["time_table"]["Tuesday"][timing] = subject_name
                elif WeekDays.Wednesday.value == idx:
                    if str(subject_name).startswith(
                        "Project Work/ Other Weekly Activities"
                    ):
                        subject_name = ""
                    time_table["time_table"]["Wednesday"][timing] = subject_name
                elif WeekDays.Thursday.value == idx:
                    if str(subject_name).startswith(
                        "Project Work/ Other Weekly Activities"
                    ):
                        subject_name = ""
                    time_table["time_table"]["Thursday"][timing] = subject_name
                elif WeekDays.Friday.value == idx:
                    if str(subject_name).startswith(
                        "Project Work/ Other Weekly Activities"
                    ):
                        subject_name = ""
                    time_table["time_table"]["Friday"][timing] = subject_name
                elif WeekDays.Saturday.value == idx:
                    if str(subject_name).startswith(
                        "Project Work/ Other Weekly Activities"
                    ):
                        subject_name = ""
                    time_table["time_table"]["Saturday"][timing] = subject_name
                elif WeekDays.Sunday.value == idx:
                    if str(subject_name).startswith(
                        "Project Work/ Other Weekly Activities"
                    ):
                        subject_name = ""
                    time_table["time_table"]["Sunday"][timing] = subject_name

        teacher_details = {}
        for tr in tables[20].find_all("tr")[2:]:
            course_code = None
            for idx, td in enumerate(tr.find_all("td")):
                div = td.find("div")
                text = div.get_text(strip=True)
                if idx == 0:
                    course_code = text
                    teacher_details[course_code] = {}
                elif idx == 1:
                    teacher_details[course_code]["course_type"] = text
                elif idx == 2:
                    teacher_details[course_code] = {"course_title": text}
                elif idx == 3:
                    teacher_details[course_code]["lectures"] = text
                elif idx == 4:
                    teacher_details[course_code]["tutorials"] = text
                elif idx == 5:
                    teacher_details[course_code]["practical"] = text
                elif idx == 6:
                    teacher_details[course_code]["credits"] = text
                elif idx == 7:
                    span = div.find_all("span")
                    teacher_details[course_code]["faculty_name"] = (
                        span[0].get_text(strip=True).split("(")[0].strip()
                    )
                    teacher_details[course_code]["cabin"] = (
                        span[0]
                        .get_text(strip=True)
                        .split("(")[-1]
                        .replace(")", "")
                        .strip()
                    )
                    teacher_details[course_code]["last_updated"] = (
                        (span[-1].get_text(strip=True)).split("::")[-1].strip()
                    )
        time_table["faculty_details"] = teacher_details
        soup.decompose()
        return time_table
    except:
        soup.decompose()
        return None
