from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant


async def get_electricity_meter(cookie):
    url = constant.UMS_ELECTRICITY_BILL_CHECK_URL
    headers = constant.USER_AGENT_ONLY
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=headers,
        ) as res:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            trs = soup.find_all(
                "tr",
                id=lambda x: x and x.startswith("ctl00_cphHeading_RadGrid1_ctl00__"),
            )
            soup.decompose()
            await session.close()
            selected_tr = trs[-2]
            tds = selected_tr.find_all("td")
            total_unit = tds[-2].get_text(strip=True)
            final_amnt = trs[-1].find_all("td")[-1].get_text(strip=True)
            final_amnt = final_amnt.replace("(", "")
            final_amnt = (final_amnt.replace(")", "")).strip()
            return {"final_amnt": final_amnt, "units_left": total_unit}


async def get_hosteler_details(cookie):
    url = constant.UMS_HOSTELER_DETAILS_URL
    headers = constant.USER_AGENT_ONLY
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=headers,
        ) as res:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            is_Hosteler = False
            profile_details = {}
            #! USER DETAILS
            student_tr_table = soup.find("tr", id="ctl00_cphHeading_TrStudentDetail")
            student_tr_divs = student_tr_table.find("table")
            reg_no = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblRegNoVal"
            ).get_text(strip=True)
            student_name = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblStuNameVal"
            ).get_text(strip=True)
            father_name = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblFatherNameVal"
            ).get_text(strip=True)
            mother_name = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblMotherNameVal"
            ).get_text(strip=True)
            gender = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblGenderVal"
            ).get_text(strip=True)
            scholarship = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblScholarshipVal"
            ).get_text(strip=True)
            programme_name = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblProgramNameVal"
            ).get_text(strip=True)
            student_status = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblStuStatusVal"
            ).get_text(strip=True)
            country = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblCountryVal"
            ).get_text(strip=True)
            admission_session = student_tr_divs.find(
                "span", id="ctl00_cphHeading_lblAdmissionSessionVal"
            ).get_text(strip=True)

            profile_details["user_details"] = {
                "registration_number": reg_no,
                "student_name": student_name,
                "father_name": father_name,
                "mother_name": mother_name,
                "gender": gender,
                "scholarship": scholarship,
                "programme_name": programme_name,
                "student_status": student_status,
                "country": country,
                "admission_session": admission_session,
            }
            hosteler_tr_table = soup.find(
                "tr", id="ctl00_cphHeading_TrStudentHostelDetail"
            )
            if hosteler_tr_table != None:
                hostel_tr_divs = hosteler_tr_table.find("table")
                hostel_name = hostel_tr_divs.find(
                    "span", id="ctl00_cphHeading_lblHostelNameVal"
                ).get_text(strip=True)
                room_type = hostel_tr_divs.find(
                    "span", id="ctl00_cphHeading_lblRoomTypeVal"
                ).get_text(strip=True)
                room_number = hostel_tr_divs.find(
                    "span", id="ctl00_cphHeading_lblRoomNoVal"
                ).get_text(strip=True)
                availing_food = hostel_tr_divs.find(
                    "span", id="ctl00_cphHeading_lblAvailingFoodVal"
                ).get_text(strip=True)
                availing_laundary = hostel_tr_divs.find(
                    "span", id="ctl00_cphHeading_lblAvailingLaundryVal"
                ).get_text(strip=True)
                is_Hosteler = True
                obj = await get_electricity_meter(cookie)
                profile_details["hostel_details"] = {
                    "hostel_name": hostel_name,
                    "room_type": room_type,
                    "room_number": room_number,
                    "availing_food": availing_food,
                    "availing_laundary": availing_laundary,
                    "units_left": obj["units_left"],
                    "final_amnt": obj["final_amnt"],
                }
            soup.decompose()
            await session.close()
            profile_details["is_hosteler"] = is_Hosteler
            return profile_details
