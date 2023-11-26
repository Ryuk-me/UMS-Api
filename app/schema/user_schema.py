from pydantic import BaseModel, ConfigDict
from typing import Union


class UserLogin(BaseModel):
    reg_no: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={"reg_no": "123456789", "password": "verySecuredPassword"}
    )


class Token(BaseModel):
    cookie: str

    model_config = ConfigDict(
        json_schema_extra={"cookie": "ASP.NET_SessionId=some_gibberish_cookies"}
    )


class UserRequests(BaseModel):
    reg_no: str
    password: str
    cookie: str

    model_config = ConfigDict(
        json_schema_extra={
            "reg_no": "123456789",
            "password": "verySecuredPassword",
            "cookie": "ASP.NET_SessionId=some_gibberish_cookies",
        }
    )


class UserOut(BaseModel):
    registration_number: str
    name: str
    program: str
    section: str
    profile_image: Union[str, None]
    dob: str
    cgpa: Union[str, None]
    phone: Union[str, None]
    agg_attendance: Union[str, None]
    roll_number: Union[str, None]
    cookie: str
