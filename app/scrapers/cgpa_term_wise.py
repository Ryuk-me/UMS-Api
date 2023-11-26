from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
import json
import re
from app.utilities.clean_str_regex import regex_replace_str


async def get_cgpa_term_wise(cookie):
    url = constant.UMS_CGPA_TERM_WISE_URL
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps({})) as res:
            html = await res.json()
            soup = BeautifulSoup(html["d"], "lxml")
            term_divs = soup.find_all("div", class_="row")
            TERM_ID = {
                1: "Term : I",
                2: "Term : II",
                3: "Term : III",
                4: "Term : IV",
                5: "Term : V",
                6: "Term : VI",
                7: "Term : VII",
                8: "Term : VIII",
                9: "Term : IX",
                10: "Term : X",
                11: "Term : XI",
                12: "Term : XII",
                13: "Term : XIII",
                14: "Term : XIV",
                15: "Term : XV",
                16: "Term : XVI",
            }
            CGPA = {"cgpa": {}}
            for term_div in term_divs:
                h4s = term_div.find_all("h4")
                term_id = h4s[0].get_text(strip=True)
                tgcpa = h4s[1].get_text(strip=True)
                term_id_nested = (term_id.split(":")[-1]).strip()
                tgcpa = ((tgcpa.split(":"))[-1]).strip()
                CGPA["cgpa"][term_id] = {
                    "term_id": term_id_nested,
                    "tgpa": tgcpa,
                    "course_grades": [],
                }
            grades_divs = soup.find_all("div", class_="table-responsive")
            for idx, grade_div in enumerate(grades_divs, start=1):
                trs = grade_div.find("tbody").find_all("tr")
                for tr in trs:
                    tds = tr.find_all("td")
                    course_name = tds[0].get_text(strip=True)
                    course_name_splitted = course_name.split(":")
                    course_name = course_name_splitted[-1].strip()
                    course_code = course_name_splitted[0].strip()
                    grade = tds[1].get_text(strip=True)
                    grade = ((grade.split(":"))[-1]).strip()
                    course_name = regex_replace_str(re.sub(" +", " ", course_name))
                    CGPA["cgpa"][TERM_ID[idx]]["course_grades"].append(
                        {
                            "course_code": course_code,
                            "course_name": course_name,
                            "grade": grade,
                        }
                    )
            soup.decompose()
            await session.close()
            return CGPA
