from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant
import requests
from app.utilities.clean_str_regex import regex_replace_str


async def get_home_page_details(cookie: str):
    url = constant.UMS_PLACEMENT_PORTAL_HOME_PAGE
    header = constant.USER_AGENT_ONLY
    header["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=header,
        ) as res:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            #! Important Div
            divs = soup.select("div.placement_ums_new_div.form_header")

            #! User Basic Details
            profile_section = soup.find("div", id="profile")
            profile_details = profile_section.find("div", class_="grid")
            uls = profile_details.find_all("ul", class_="personal-info")
            left_details_lis = uls[0].find_all("li")
            right_details_lis = uls[1].find_all("li")

            user_details = {
                "registration_number": left_details_lis[0]
                .find("span")
                .get_text(strip=True),
                "placement_id": left_details_lis[1].find("span").get_text(strip=True),
                "basic_details": regex_replace_str(
                    regex_replace_str(
                        left_details_lis[2].find("span").get_text(strip=True)
                    )
                ),
                "placement_services_status": regex_replace_str(
                    left_details_lis[3].find("span").get_text(strip=True)
                ),
                "opportunity_start_date": regex_replace_str(
                    left_details_lis[4].find("span").get_text(strip=True)
                ),
                "email": regex_replace_str(
                    left_details_lis[5].find("span").get_text(strip=True)
                ),
                "contact_no": regex_replace_str(
                    left_details_lis[6].find("span").get_text(strip=True)
                ),
                "program": regex_replace_str(
                    left_details_lis[7].find("span").get_text(strip=True)
                ),
                "company_selected_in": regex_replace_str(
                    left_details_lis[8].find("span").get_text(strip=True)
                ),
                #! Right side data scraping
                "cgpa": regex_replace_str(
                    right_details_lis[0].find("span").get_text(strip=True)
                ),
                "reappear_or_backlog": regex_replace_str(
                    right_details_lis[1].find("span").get_text(strip=True)
                ),
                "pep_fee_details": regex_replace_str(
                    right_details_lis[2].find("span").get_text(strip=True)
                ),
                "pep_fee_payment_date": regex_replace_str(
                    right_details_lis[3].find("span").get_text(strip=True)
                ),
                "x_marks": regex_replace_str(
                    right_details_lis[4].find("span").get_text(strip=True)
                ),
                "xii_marks": regex_replace_str(
                    right_details_lis[5].find("span").get_text(strip=True)
                ),
                "graduation_marks": regex_replace_str(
                    right_details_lis[6].find("span").get_text(strip=True)
                ),
                "diploma_marks": regex_replace_str(
                    right_details_lis[7].find("span").get_text(strip=True)
                ),
            }

            #! TPC DETAILS
            user_details["tpc_coordinators"] = []
            tpc_employee_details = divs[0].next_sibling.find_next("table")
            for tr in tpc_employee_details.find_all("tr")[1:]:
                tds = tr.find_all("td")
                mentor_name = regex_replace_str(
                    tds[1].find("span").get_text(strip=True)
                )
                try:
                    mentor_email = regex_replace_str(
                        tds[2].find("span").get_text(strip=True)
                    )
                except:
                    mentor_email = None
                phone_number = regex_replace_str(
                    tds[3].find("span").get_text(strip=True)
                )
                mentor_seating_place = regex_replace_str(
                    tds[4].find("span").get_text(strip=True)
                )
                role = regex_replace_str(tds[0].get_text(strip=True))
                user_details["tpc_coordinators"].append(
                    {
                        "name": mentor_name,
                        "email": mentor_email,
                        "phone_number": phone_number,
                        "cabin": mentor_seating_place,
                        "role": role,
                    }
                )
            ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #! Upcoming Placement Drives Details
            upcoming_placemnet_drives = soup.find(
                "table", class_="main_table main_table12"
            )
            upcoming_drives = []
            if upcoming_placemnet_drives is not None:
                upcoming_placemnet_drives_trs = upcoming_placemnet_drives.find_all("tr")
                for tr in upcoming_placemnet_drives_trs[1:]:
                    tds = tr.find_all("td")
                    drive_date = regex_replace_str(tds[0].get_text(strip=True))
                    register_by = regex_replace_str(tds[1].get_text(strip=True))
                    company = regex_replace_str(tds[2].get_text(strip=True))
                    job_profile = (
                        "https://ums.lpu.in/Placements/" + tds[3].find("a")["href"]
                    )

                    status = regex_replace_str(tds[4].get_text(strip=True))
                    registered = regex_replace_str(tds[5].get_text(strip=True))
                    try:
                        hall_ticket = tds[6].find("a")["href"]
                    except:
                        hall_ticket = None
                    upcoming_drives.append(
                        {
                            "drive_date": drive_date,
                            "register_by": register_by,
                            "company": company,
                            "job_profile": requests.utils.requote_uri(job_profile),
                            "status": status,
                            "registered": registered,
                            "hall_ticket": (
                                requests.utils.requote_uri(
                                    "https://ums.lpu.in/Placements/" + hall_ticket
                                )
                                if hall_ticket is not None
                                else hall_ticket
                            ),
                        }
                    )
            #! Total drives Held
            total_drives_held_data = (
                divs[4]
                .next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.find_next(
                    "table"
                )
                .find("table")
                .find("table")
            )
            drives_count = []
            for tr in total_drives_held_data.find_all("tr"):
                tds = tr.find_all("td")
                label = regex_replace_str(tds[0].get_text(strip=True))
                counter = tds[1].get_text(strip=True)
                drives_count.append({"label": label, "count": counter})

            user_details["upcoming_drives"] = upcoming_drives
            user_details["drives_held"] = drives_count

            #! Fines if any
            user_details["fines"] = []
            fine_details = soup.find("table", id="ctl00_ContentPlaceHolder1_gdFine")
            if fine_details is not None:
                for tr in fine_details.find_all("tr")[1:]:
                    tds = tr.find_all("td")
                    company_name = regex_replace_str(tds[0].get_text(strip=True))
                    drive_round = regex_replace_str(tds[1].get_text(strip=True))
                    fine_instance = regex_replace_str(tds[2].get_text(strip=True))
                    fine_amount = regex_replace_str(tds[3].get_text(strip=True))
                    fine_paid = regex_replace_str(tds[4].get_text(strip=True))
                    receipt_no = regex_replace_str(tds[5].get_text(strip=True))
                    drive_date = regex_replace_str(tds[6].get_text(strip=True))
                    user_details["fines"].append(
                        {
                            "company_name": company_name,
                            "drive_round": drive_round,
                            "fine_instance": fine_instance,
                            "fine_amount": fine_amount,
                            "fine_paid": fine_paid,
                            "recepit_number": receipt_no,
                            "drive_date": drive_date,
                        }
                    )
            await session.close()
            return user_details


async def get_placement_drives(cookie):
    url = constant.UMS_PLACEMENT_PORTAL_DRIVE_REGISTRATION
    headers = constant.USER_AGENT_ONLY
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as res:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            table = soup.find("table", id="ctl00_ContentPlaceHolder1_gdvPlacement")
            drive_details = {"drive_details": []}
            if table is not None:
                trs = table.find_all("tr")
                for tr in trs[1:-2]:
                    tds = tr.find_all("td")
                    drive_code = regex_replace_str(tds[0].get_text(strip=True))
                    drive_date = regex_replace_str(tds[1].get_text(strip=True))
                    register_by = regex_replace_str(tds[2].get_text(strip=True))
                    company = regex_replace_str(tds[3].get_text(strip=True))
                    streams_eligible = regex_replace_str(tds[4].get_text(strip=True))
                    venue = regex_replace_str(tds[5].get_text(strip=True))
                    job_profile = (
                        "https://ums.lpu.in/Placements/" + tds[6].find("a")["href"]
                    )
                    status = regex_replace_str(tds[7].get_text(strip=True))
                    is_eligible = regex_replace_str(tds[8].get_text(strip=True))
                    registered = regex_replace_str(tds[9].get_text(strip=True))
                    drive_details["drive_details"].append(
                        {
                            "drive_code": drive_code,
                            "drive_date": drive_date,
                            "register_by": register_by,
                            "company": company,
                            "streams_eligible": streams_eligible,
                            "venue": venue,
                            "job_profile": requests.utils.requote_uri(job_profile),
                            "status": status,
                            "is_eligible": is_eligible,
                            "registered": registered,
                        }
                    )
                await session.close()
            return drive_details
