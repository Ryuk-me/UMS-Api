from bs4 import BeautifulSoup
import aiohttp
from app.constants import constant


async def get_hostel_leave_slip(cookie):
    url = constant.UMS_HOSTEL_LEAVE_SLIP_URL
    headers = constant.USER_AGENT_ONLY
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=headers,
        ) as res:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            selected_table = soup.find("table", id="ctl00_cphHeading_tblSlipData")
            if selected_table == None:
                return None
            trs = selected_table.find_all("tr")
            lpu_name = trs[0]
            lovely = lpu_name.find("strong").get_text(strip=True)
            profile_image = lpu_name.find("img", id="ctl00_cphHeading_Image1")["src"]
            leave_type = lpu_name.find("span", id="ctl00_cphHeading_lblLName").get_text(
                strip=True
            )
            barcode = trs[5].find("img", id="ctl00_cphHeading_imgBarcodefile")["src"]
            leave_id = (
                trs[7].find("span", id="ctl00_cphHeading_lblLid").get_text(strip=True)
            )
            reg_no = (
                trs[8].find("span", id="ctl00_cphHeading_lblRegNo").get_text(strip=True)
            )
            name = (
                trs[9].find("span", id="ctl00_cphHeading_lblName").get_text(strip=True)
            )
            date_of_apply = (
                trs[10]
                .find("span", id="ctl00_cphHeading_lblDateofapply")
                .get_text(strip=True)
            )
            date_of_leaving = (
                trs[11]
                .find("span", id="ctl00_cphHeading_lblDateofleaveing")
                .get_text(strip=True)
            )
            date_of_return = (
                trs[12]
                .find("span", id="ctl00_cphHeading_lblDateofreturn")
                .get_text(strip=True)
            )
            checkout_time = (
                trs[13]
                .find("span", id="ctl00_cphHeading_lblcheckouttime")
                .get_text(strip=True)
            )
            contact_no = (
                trs[15]
                .find("span", id="ctl00_cphHeading_lblmobile")
                .get_text(strip=True)
            )
            hostel = (
                trs[16]
                .find("span", id="ctl00_cphHeading_lblhostel")
                .get_text(strip=True)
            )
            hostel_room_no = (
                trs[17]
                .find("span", id="ctl00_cphHeading_lblroomno")
                .get_text(strip=True)
            )
            await session.close()
            soup.decompose()
            return {
                "lovely": lovely,
                "profile_image": profile_image,
                "leave_type": leave_type,
                "barcode": barcode,
                "leave_id": leave_id,
                "reg_no": reg_no,
                "name": name,
                "date_of_apply": date_of_apply,
                "date_of_leaving": date_of_leaving,
                "date_of_return": date_of_return,
                "checkout_time": checkout_time,
                "contact_no": contact_no,
                "hostel": hostel,
                "hostel_room_no": hostel_room_no,
            }
