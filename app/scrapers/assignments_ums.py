from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
from requests.utils import requote_uri
import re
from app.utilities.clean_str_regex import regex_replace_str


async def get_all_assignments_and_marks(cookie):
    url = constant.UMS_ASSIGMENTS_MARKS_URL
    headers = constant.USER_AGENT_ONLY
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            __VSTATE = soup.find("input", {"id": "__VSTATE"})["value"]
            __EVENTVALIDATION = soup.find("input", {"id": "__EVENTVALIDATION"})["value"]
            payload = {
                "__VSTATE": __VSTATE,
                "__VIEWSTATE": "",
                "__EVENTVALIDATION": __EVENTVALIDATION,
                "ctl00$cphHeading$Button1": "View All",
            }
            soup.decompose()
            headers = constant.USER_AGENT_FORM_URL_ENCODED
            headers["Cookie"] = cookie
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=payload) as res:
                    assignments = {"theory": [], "practical": []}
                    html = await res.text()
                    soup = BeautifulSoup(html, "lxml")
                    try:
                        assigment_table = soup.find(
                            "table", id="ctl00_cphHeading_rgAssignment_ctl00"
                        ).find("tbody")
                    except AttributeError:
                        soup.decompose()
                        await session.close()
                        return assignments
                    trs = assigment_table.find_all(
                        "tr",
                        id=lambda x: x
                        and x.startswith("ctl00_cphHeading_rgAssignment_ctl00__"),
                    )
                    for tr in trs:
                        tds = tr.find_all("td")
                        course_code = tds[1].get_text(strip=True)
                        faculty_name = tds[2].get_text(strip=True)
                        upload_date = tds[3].get_text(strip=True)
                        submission_date = tds[4].get_text(strip=True)
                        _type = tds[5].get_text(strip=True)
                        topic = tds[6].get_text(strip=True)
                        comments = tds[7].get_text(strip=True)
                        submission_type = tds[8].get_text(strip=True)
                        marks_obtained = tds[9].get_text(strip=True)
                        total_marks = tds[10].get_text(strip=True)
                        teacher_comments = tds[11].get_text(strip=True)
                        assignment_download_url = ""
                        assignment_uploaded_by_student = ""
                        try:
                            assignment_download_url = tds[12].find("input")["text"]
                            if assignment_download_url != "":
                                assignment_download_url = (
                                    "http://assignments.lpu.in/Teacher/"
                                    + requote_uri(assignment_download_url)
                                )
                        except:
                            pass
                        try:
                            assignment_uploaded_by_student = tds[13].find("input")[
                                "text"
                            ]
                            if assignment_uploaded_by_student != "":
                                assignment_uploaded_by_student = (
                                    "http://assignments.lpu.in/Teacher/"
                                    + requote_uri(assignment_uploaded_by_student)
                                )
                        except:
                            pass
                        comments = regex_replace_str(comments)
                        teacher_comments = regex_replace_str(comments)
                        comments = re.sub(" +", " ", comments)
                        teacher_comments = re.sub(" +", " ", teacher_comments)
                        obj = {}
                        obj["course_code"] = course_code
                        obj["faculty_name"] = faculty_name
                        obj["upload_date"] = upload_date
                        obj["submission_date"] = submission_date
                        obj["type"] = _type
                        obj["topic"] = topic
                        obj["comments"] = comments
                        obj["submission_type"] = submission_type
                        obj["marks_obtained"] = marks_obtained
                        obj["total_marks"] = total_marks
                        obj["teacher_comments"] = teacher_comments
                        obj["assignment_download_url"] = assignment_download_url
                        obj[
                            "assignment_uploaded_by_student"
                        ] = assignment_uploaded_by_student
                        assignments["theory"].append(obj)

                    try:
                        practical_table = soup.find(
                            "table", id="ctl00_cphHeading_gvPracticalComponent_ctl00"
                        ).find("tbody")
                    except AttributeError:
                        soup.decompose()
                        await session.close()
                        return assignments
                    trs = practical_table.find_all(
                        "tr",
                        id=lambda x: x
                        and x.startswith(
                            "ctl00_cphHeading_gvPracticalComponent_ctl00__"
                        ),
                    )
                    for tr in trs:
                        tds = tr.find_all("td")
                        course_code = tds[1].get_text(strip=True)
                        faculty_name = tds[2].get_text(strip=True)
                        title = tds[3].get_text(strip=True)
                        comp_1_name = tds[4].get_text(strip=True)
                        comp_1_marks = tds[5].get_text(strip=True)
                        comp_1_total_marks = tds[6].get_text(strip=True)

                        comp_2_name = tds[7].get_text(strip=True)
                        comp_2_marks = tds[8].get_text(strip=True)
                        comp_2_total_marks = tds[9].get_text(strip=True)

                        comp_3_name = tds[10].get_text(strip=True)
                        comp_3_marks = tds[11].get_text(strip=True)
                        comp_3_total_marks = tds[12].get_text(strip=True)

                        comp_4_name = tds[13].get_text(strip=True)
                        comp_4_marks = tds[14].get_text(strip=True)
                        comp_4_total_marks = tds[15].get_text(strip=True)

                        marks_obtained = tds[16].get_text(strip=True)
                        total_marks = tds[17].get_text(strip=True)
                        assignment_uploaded_by_student = ""
                        try:
                            assignment_uploaded_by_student = tds[18].find("a")["href"]
                            assignment_uploaded_by_student = (
                                "https://ums.lpu.in/"
                                + requote_uri(assignment_uploaded_by_student)
                            )
                        except:
                            pass

                        assignments["practical"].append(
                            {
                                "course_code": course_code,
                                "faculty_name": faculty_name,
                                "title": title,
                                "comp_1_name": comp_1_name,
                                "comp_1_marks": comp_1_marks,
                                "comp_1_total_marks": comp_1_total_marks,
                                "comp_2_name": comp_2_name,
                                "comp_2_marks": comp_2_marks,
                                "comp_2_total_marks": comp_2_total_marks,
                                "comp_3_name": comp_3_name,
                                "comp_3_marks": comp_3_marks,
                                "comp_3_total_marks": comp_3_total_marks,
                                "comp_4_name": comp_4_name,
                                "comp_4_marks": comp_4_marks,
                                "comp_4_total_marks": comp_4_total_marks,
                                "marks_obtained": marks_obtained,
                                "total_marks": total_marks,
                                "assignment_uploaded_by_student": assignment_uploaded_by_student,
                            }
                        )
                    soup.decompose()
                    await session.close()
                    return assignments
