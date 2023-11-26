import aiohttp
from app.constants import constant
import json


async def get_all_annoucements(cookie):
    url = constant.UMS_ANNOUNCEMENT_URL
    headers = constant.USER_AGENT_JSON
    headers["Cookie"] = cookie
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, headers=headers, data=json.dumps({"LoginId": "Reg", "Type": "S"})
        ) as res:
            res_json = await res.json()
            res_json = res_json["d"]
            announcement_list = {"annoucements": []}
            for annoucement in res_json:
                if annoucement["categorycode"] == "AC":
                    category_code = "Academic"
                elif annoucement["categorycode"] == "PL":
                    category_code = "Placement"
                elif annoucement["categorycode"] == "EX":
                    category_code = "Examination"
                elif annoucement["categorycode"] == "RE":
                    category_code = "Research"
                elif annoucement["categorycode"] == "AM":
                    category_code = "Administrative/Misc"
                elif annoucement["categorycode"] == "CU":
                    category_code = "Co-Curricular/Sports/Cultural"
                else:
                    category_code = annoucement["categorycode"]

                announcement_list["annoucements"].append(
                    {
                        "subject": annoucement["subject"],
                        "announcement_id": annoucement["announcementid"],
                        "time": annoucement["time"],
                        "date": annoucement["date"],
                        "uploaded_by": annoucement["uploadedby"],
                        "employee_name": annoucement["employeename"],
                        "header_date": annoucement["HeaderDate"],
                        "category_name": category_code,
                        "category_code": annoucement["categorycode"],
                    }
                )
            await session.close()
            return announcement_list
